# coding=utf-8
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import waitress
import threading
import logging
import uuid
import time
import os
from datetime import datetime

import cv2
import json
import redis
import psycopg2
from psycopg2.extras import DictCursor
import shutil

import sys
import yaml
import argparse
from PIL import Image
import io
import time
import subprocess

from PyPDF2 import PdfReader
import fitz
import win32print

# --------------------- APP 全局配置 ---------------------
app = Flask(
    __name__,
    static_folder="templates",
    static_url_path=""
)
CORS(app=app)

# 配置上传目录和队列名称
UPLOAD_FOLDER = "print_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
PRINT_QUEUE = "print_queue"

logger = logging.Logger("WSGI")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def get_options():
    '''获取所有的 YAML 文件'''
    args = argparse.ArgumentParser(description="打印系统后端配置")
    args.add_argument("--config", type=str, default="config.yaml", help="输入配置 YAML 文件")
    args.add_argument("--debug", action='store_true', help="DEBUG 模式")
    return args.parse_args()

# --------------------- DATABASE 全局配置 ---------------------
opt = get_options()
data = None
with open(opt.config, mode='r', encoding='utf-8') as f:
    data = yaml.safe_load(f.read())

if data is None:
    raise RuntimeError("读取 YAML 文件失败")

logger.info("读取到配置文件: {}".format(data))

DB_CONFIG = {
    'host': data['pgsql']['host'],
    'port': data['pgsql']['port'],
    'database': data['pgsql']['db'],
    'user': data['pgsql']['usr'],
    'password': data['pgsql']['pwd']
}

RS_CONFIG = {
    'host': data['redis']['host'],
    'port': data['redis']['port'],
    'db': data['redis']['db'],
    'password': data['redis']['pwd']
}

redis_pool = redis.ConnectionPool(** RS_CONFIG)
redis_client = redis.Redis(connection_pool=redis_pool)

# --------------------- 打印相关功能实现 ---------------------
def is_printer_available(printer_name=None):
    if printer_name is None:
        try:
            printer_name = win32print.GetDefaultPrinter()
        except:
            return False
    
    try:
        handle = win32print.OpenPrinter(printer_name)
        printer_info = win32print.GetPrinter(handle, 2)
        status = printer_info['Status']
        win32print.ClosePrinter(handle)

        non_available_status = (
            win32print.PRINTER_STATUS_PAUSED |
            win32print.PRINTER_STATUS_ERROR |
            win32print.PRINTER_STATUS_OFFLINE |
            win32print.PRINTER_STATUS_PAPER_OUT |
            win32print.PRINTER_STATUS_NO_TONER |
            win32print.PRINTER_STATUS_OUTPUT_BIN_FULL |
            win32print.PRINTER_STATUS_DOOR_OPEN |
            win32print.PRINTER_STATUS_NOT_AVAILABLE
        )

        # 若没有任何不可打印状态，则返回True
        return (status & non_available_status) == 0
    except Exception as e:
        print(f"获取打印机状态异常：{e}")
        return False

def get_file_type(file_data):
    """根据文件头部信息判断文件类型"""
    # PDF文件头部标识
    if file_data.startswith(b'%PDF-'):
        return 'pdf'
    # 尝试用PIL识别图片类型
    try:
        Image.open(io.BytesIO(file_data))
        return 'image'
    except:
        return 'unknown'


# 修改：支持PDF和图片的转换函数
def process_file(file_data, job_id):
    """处理文件，返回文件路径和类型"""
    file_type = get_file_type(file_data)
    
    if file_type == 'pdf':
        return process_pdf(file_data, job_id)
    elif file_type == 'image':
        return process_image(file_data, job_id)
    else:
        raise ValueError("不支持的文件类型，仅支持图片和PDF")


# 新增：处理PDF文件
def process_pdf(pdf_data, job_id):
    """处理PDF文件，返回保存路径"""
    pdf_filename = f"{job_id}.pdf"
    filepath = os.path.join(UPLOAD_FOLDER, pdf_filename)
    
    # 直接保存PDF文件
    with open(filepath, 'wb') as f:
        f.write(pdf_data)
    
    # 可以在这里添加PDF预览图生成逻辑（可选）
    # 例如生成第一页的预览图
    try:
        reader = PdfReader(io.BytesIO(pdf_data))
        page_count = len(reader.pages)
    except:
        page_count = 0
    
    return filepath, 'pdf', page_count


# 修改：处理图片文件（原convert_to_png逻辑）
def process_image(image_data, job_id):
    """处理图片文件，转换为PNG并保存"""
    img = Image.open(io.BytesIO(image_data))
    
    # 转换为RGBA模式（处理透明背景）
    if img.mode in ('RGBA', 'LA'):
        background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
        background.paste(img, img.split()[-1])
        img = background
    
    # 转换为PNG格式
    png_filename = f"{job_id}.png"
    filepath = os.path.join(UPLOAD_FOLDER, png_filename)
    img.save(filepath, 'PNG')
    
    return filepath, 'image', 1  # 图片视为1页

def convert_to_png(image_data):
    """将图片数据转换为 PNG 格式"""
    try:
        image = Image.open(io.BytesIO(image_data))
        
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        
        output = io.BytesIO()
        image.save(output, format="PNG")
        output.seek(0)
        return output.read()
    except Exception as e:
        logger.error(f"图片转换失败: {str(e)}")
        raise

def save_image_to_local(image_data, filename):
    """保存图片到本地"""
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(image_data)
    return filepath

def printer_function(printer_id=1, filepath=None, filetype='pdf', print_options:dict={'copies':1, 'duplex':False}):
    """
    打印过程，调用 C# 程序进行打印。

    :param printer_id: 打印机ID (用于从数据库获取打印机名称)
    :param filepath: 文件路径
    :param filetype: 文件类型 ('image' 或 'pdf')
    :param print_options: 打印选项字典，包含 'copies', 'duplex', 'vh' 等键
    """
    logger.info(f"开始打印任务 {printer_id}，文件路径: {filepath}，文件类型: {filetype}")
    flag = True if filepath is not None else False

    if filepath is None:
        logger.error("文件路径为空，无法打印。")
        return flag
    filepath = os.path.abspath(filepath) # 转为绝对路径
    logger.info(f"打印文件绝对路径: {filepath}")
    
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=DictCursor)
        
        cursor.execute("SELECT * FROM printer WHERE id = %s", (printer_id,))
        printer = cursor.fetchone()
        if not printer:
            logger.error(f"未找到ID为 {printer_id} 的打印机。")
            return False
        printer_name = printer['name']
        logger.info(f"获取到打印机名称: {printer_name}")

        copies = print_options.get('copies', 1)
        duplex = print_options.get('duplex', False)
        vh = print_options.get('vh', 'h')  # h 表示纵向打印, v 表示横向打印

        ps_commands = []
        print_cmd = ''
        
        if filetype == 'image':
            # 读取 PDF 并且写入 YAML 文件
            BASE_DIR = os.environ["NANOKA_PATH"] # 缓存主目录
            printer_path = os.path.join(BASE_DIR, f"{printer_id}") # 打印机任务目录
            if not os.path.exists(printer_path):
                os.makedirs(printer_path, exist_ok=True)

            main_path = os.path.join(printer_path, "Front")
            if not os.path.exists(main_path):
                os.makedirs(main_path, exist_ok=True)

            task_id = str(uuid.uuid4())
            yaml_path = os.path.join(BASE_DIR, f"{task_id}.yaml") # 放在缓存主目录下

            # 将文件拷贝进具体文件夹
            shutil.copy(filepath, main_path)

            with open(yaml_path, 'w+', encoding='gbk') as yf:
                yaml_content = {
                    'id': printer_id,
                    'printer': printer_name,
                    'file': os.path.abspath(os.path.join(main_path, os.path.basename(filepath))),
                    'filetype': 'image',
                    'copies': copies,
                    'duplex': 1 if duplex else 0,
                    'route': vh
                }
                yaml.dump(yaml_content, yf, allow_unicode=True)
                logger.info(f"已生成打印任务 YAML 文件: {yaml_path}")

            # 命令行为: Printer.exe --yaml "C:\Path\To\Task.yaml"
            print_cmd += f'cd "D:\\Code\\C#\\Printer\\bin\\Release"; '
            print_cmd += f'& ".\\Printer.exe" --yaml {os.path.abspath(yaml_path)}'
            ps_commands.append(print_cmd)
            
        elif filetype == 'pdf':
            # 读取 PDF 并且写入 YAML 文件
            BASE_DIR = os.environ["NANOKA_PATH"] # 缓存主目录
            printer_path = os.path.join(BASE_DIR, f"{printer_id}") # 打印机任务目录
            if not os.path.exists(printer_path):
                os.makedirs(printer_path, exist_ok=True)

            task_id = str(uuid.uuid4())
            yaml_path = os.path.join(BASE_DIR, f"{task_id}.yaml")

            # 不需要手动切割正反，打印机里都有！！！
            front_dir = os.path.join(printer_path, "Front")
            if not os.path.exists(front_dir):
                os.makedirs(front_dir, exist_ok=True)
            
            # 使用 PyMuPDF 或其他库将 PDF 页面转换为图片
            fitz_doc = fitz.open(filepath)
            for page_num in range(len(fitz_doc)):
                page = fitz_doc.load_page(page_num)
                matrix = fitz.Matrix(2.5, 2.5)
                pix = page.get_pixmap(matrix=matrix)
                img_data = pix.tobytes("png")
                
                image_filename = "{}.png".format(str(page_num + 1).zfill(4))
                image_path = os.path.join(front_dir, image_filename)
                with open(image_path, 'wb') as img_f:
                    img_f.write(img_data)
                logger.info(f"已保存 PDF 页面为图片: {image_path}")

            with open(yaml_path, 'w+', encoding='gbk') as yf:
                yaml_content = {
                    'id': printer_id,
                    'printer': printer_name,
                    'file': printer_path,
                    'filetype': 'pdf',
                    'copies': copies,
                    'duplex': 1 if duplex else 0,
                    'route': vh,
                    'pagenum': len(fitz_doc)
                }
                yaml.dump(yaml_content, yf, allow_unicode=True)
                logger.info(f"已生成打印任务 YAML 文件: {yaml_path}")

            # 命令行为: Printer.exe --yaml "C:\Path\To\Task.yaml"
            print_cmd += f'cd "D:\\Code\\C#\\Printer\\bin\\Release"; '
            print_cmd += f'& ".\\Printer.exe" --yaml {os.path.abspath(yaml_path)}'
            ps_commands.append(print_cmd)
        
        else:
            logger.error(f"不支持的文件类型: {filetype}")
            return False

        full_ps_command = '; '.join(ps_commands)
        
        logger.debug(f"执行 PowerShell 命令: {full_ps_command}")
        
        # # 使用 PS 打印程序
        result = subprocess.run(
            ["powershell.exe", "-Command", full_ps_command],
            capture_output=True,
            text=True,
            encoding='gbk'
        )

        if result.returncode == 0:
            logger.info(f"打印任务 {printer_id} 已成功发送。")
            if result.stdout:
                logger.debug(f"PowerShell 标准输出: {result.stdout}")
        else:
            logger.error(f"打印任务 {printer_id} 失败。")
            logger.error(f"PowerShell 错误输出: {result.stderr}")
            flag = False

    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"打印任务 {printer_id} 发生异常: {e}", exc_info=True)
        flag = False
    finally:
        if conn:
            cursor.close()
            conn.close()
    
    logger.info(f"任务 {printer_id} 处理完成")
    return flag

def print_worker():
    """打印队列工作线程（适配JSON格式存储）"""
    logger.info("打印工作线程启动")
    while True:
        try:
            # 从队列获取任务（阻塞方式）
            _, job_data = redis_client.blpop(PRINT_QUEUE)
            job_id = job_data.decode('utf-8')
            logger.info(f"获取到打印任务: {job_id}")
            
            # 获取任务信息（JSON格式）
            job_key = f"print_job:{job_id}"
            job_json = redis_client.hget(job_key, "info")
            if not job_json:
                logger.warning(f"任务 {job_id} 信息不存在")
                continue
                
            # 解析JSON数据
            job_info = json.loads(job_json.decode('utf-8'))

            # 从 Redis 拿出来以下数据
            # logger.info(f"任务信息: {job_info}") # {'filename': 'workflow.png', 'filepath': 'print_uploads\\fe8ee0bd-95c6-4984-b976-3126d04dd041.png', 'file_type': 'image', 'page_count': 1, 'status': 'pending', 'submitted_at': '2025-11-18T15:20:35.521206', 'username': 'unknown', 'copies': '1', 'printer_id': '1', 'print_mode': '1', 'vh': 'h'}

            # 获取文件路径
            filepath = job_info.get('filepath', '')
            if not filepath or not os.path.exists(filepath):
                logger.error(f"任务 {job_id} 的文件不存在: {filepath}")
                # 更新任务状态为失败
                job_info['status'] = 'failed'
                job_info['error'] = '文件不存在'
                redis_client.hset(job_key, "info", json.dumps(job_info))
                redis_client.expire(job_key, 300)  # 5分钟过期
                continue
                
            # 执行打印操作
            filetype = job_info.get('file_type', '')
            success = printer_function(job_info.get("printer_id", 1), filepath, filetype, 
                                       {'copies': int(job_info.get('copies', 1)), 
                                        'duplex': job_info.get('print_mode', '1') == '2', # 2 表示双面打印
                                        'vh': job_info.get('vh', 'h')})
            
            if success:
                # 打印成功 - 删除本地文件
                if os.path.exists(filepath):
                    os.remove(filepath)
                    logger.info(f"已删除本地缓存文件: {filepath}")
                
                # 更新任务状态
                job_info['status'] = 'completed'
                job_info['completed_at'] = datetime.now().isoformat()
                redis_client.hset(job_key, "info", json.dumps(job_info))
                redis_client.expire(job_key, 300)
                
                logger.info(f"任务 {job_id} 已完成并清理")
            else:
                # 打印失败
                job_info['status'] = 'failed'
                job_info['error'] = '打印过程失败'
                job_info['failed_at'] = datetime.now().isoformat()
                redis_client.hset(job_key, "info", json.dumps(job_info))
                redis_client.expire(job_key, 300)
                logger.error(f"任务 {job_id} 打印失败")
                
        except Exception as e:
            logger.error(f"打印工作线程错误: {str(e)}")
            time.sleep(1)

# Work process 1 —— 只有一个工作线程，不然可能出现竞争
threading.Thread(target=print_worker, daemon=True).start()

# --------------------- APP router 全局配置 ---------------------
@app.route("/")
def root():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        cursor.execute(
            "SELECT * FROM username WHERE usr = %s AND pwd = %s",
            (username, password)
        )
        user = cursor.fetchone()
        if user:
            token = str(uuid.uuid4())
            return jsonify({
                'username': user['usr'],
                'token': token,
                'message': '登录成功'
            }), 200
        else:
            return jsonify({'error': '用户名或密码错误'}), 401
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/printers', methods=['GET'])
def get_printers():
    """获取可用打印机列表"""
    printers = []
    flag = True
    error_msg = "" 

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=DictCursor)
    try:
        # 查询所有打印机（ID、名称），并逐个检查状态+更新
        cursor.execute("SELECT id, name FROM printer ORDER BY id;")
        det = cursor.fetchall()

        # 遍历打印机，检查状态并更新数据库
        for line in det:
            printer_id = line['id']
            printer_name = line['name']
            is_available = is_printer_available(printer_name=printer_name)
            sts = 'online' if is_available else 'offline'
            
            cursor.execute(
                "UPDATE printer SET status = %s WHERE name = %s;",
                (sts, printer_name)
            )

        conn.commit()

        cursor.execute(
            "SELECT id, name, location, type, status FROM printer ORDER BY id;"
        )
        matrix = cursor.fetchall()
        for line in matrix:
            printers.append({
                "id": line['id'],
                "name": line['name'],
                "location": line['location'],
                "type": line['type'],
                "status": line['status']
            })

    except Exception as e:
        flag = False
        error_msg = str(e)
        conn.rollback()
        logger.error(f"获取打印机列表失败: {error_msg}")
    finally:
        cursor.close()
        conn.close()

    if flag:
        return jsonify({"printers": printers}), 200
    else:
        # 使用存储的 error_msg，避免 e 未定义
        return jsonify({'error': error_msg}), 500

@app.route('/print/upload', methods=['POST'])
def upload_print_file():
    """上传打印文件并加入队列（支持多文件和PDF）"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': '未找到文件'}), 400

        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': '未选择有效文件'}), 400
        
        job_ids = []
        for file in files:
            if file.filename == '':
                continue
            
            file_data = file.read()
            
            job_id = str(uuid.uuid4())
            
            try:
                # 处理文件（支持图片和PDF）
                filepath, file_type, page_count = process_file(file_data, job_id)
            except Exception as e:
                return jsonify({'error': f'文件 {file.filename} 处理失败: {str(e)}'}), 400
                
            # 构建完整的任务信息字典
            job_info = {
                "filename": file.filename,
                "filepath": filepath,
                "file_type": file_type,
                "page_count": page_count,
                "status": "pending",
                "submitted_at": datetime.now().isoformat(),
                "username": request.args.get('username', 'unknown'),
                "copies": request.form.get('copies', 1),
                "printer_id": request.form.get('printer_id', ''),
                "print_mode": request.form.get('print_mode', '1'),
                "vh": request.form.get('flat_mode', 'h')
            }
            
            # 存储任务信息到Redis（单个字段存储JSON字符串）
            # 这里使用"info"作为唯一字段名，值为JSON字符串
            redis_client.hset(
                f"print_job:{job_id}",
                "info",
                json.dumps(job_info)
            )
            redis_client.expire(f"print_job:{job_id}", 300)
            # 将任务加入打印队列
            redis_client.rpush(PRINT_QUEUE, job_id)
            redis_client.expire(PRINT_QUEUE, 300)
            
            job_ids.append(job_id)
            logger.info(f"文件 {file.filename} 已上传并加入打印队列，任务ID: {job_id}")
        
        return jsonify({
            'success': True,
            'job_ids': job_ids,
            'message': f'成功上传 {len(job_ids)} 个文件并加入打印队列'
        }), 200
        
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/print/jobs', methods=['GET'])
def get_print_jobs():
    """获取当前打印任务列表（适配JSON格式存储）"""
    try:
        # 获取所有任务ID
        job_ids = [key.decode('utf-8').split(':')[1] 
                  for key in redis_client.keys('print_job:*')]
        
        jobs = []
        for job_id in job_ids:
            # 从Redis获取JSON字符串并解析
            job_json = redis_client.hget(f"print_job:{job_id}", "info")
            if not job_json:
                continue
                
            # 解析JSON
            job_info = json.loads(job_json.decode('utf-8'))
            
            # 构建返回的任务信息
            jobs.append({
                'job_id': job_id,
                'filename': job_info.get('filename', ''),
                'file_type': job_info.get('file_type', ''),
                'page_count': job_info.get('page_count', 0),
                'status': job_info.get('status', ''),
                'submitted_at': job_info.get('submitted_at', ''),
                'completed_at': job_info.get('completed_at') or None
            })
            
        # 按提交时间排序
        jobs.sort(key=lambda x: x['submitted_at'], reverse=True)
        
        return jsonify({'jobs': jobs}), 200
        
    except Exception as e:
        logger.error(f"获取打印任务失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# 其实这一部分没接进去，万一这打印机能停止呢？反正现在好像是不太行
@app.route('/print/jobs/<job_id>/cancel', methods=['POST'])
def cancel_print_job(job_id):
    """取消打印任务（适配JSON格式存储）"""
    try:
        job_key = f"print_job:{job_id}"
        if not redis_client.exists(job_key):
            return jsonify({'error': '任务不存在'}), 404
            
        # 获取并解析任务信息
        job_json = redis_client.hget(job_key, "info")
        if not job_json:
            return jsonify({'error': '任务信息损坏'}), 400
            
        job_info = json.loads(job_json.decode('utf-8'))
        
        # 检查任务状态
        if job_info['status'] in ['completed', 'failed']:
            return jsonify({'error': f'任务已{job_info["status"]}，无法取消'}), 400
            
        # 更新任务状态
        job_info['status'] = 'cancelled'
        job_info['cancelled_at'] = datetime.now().isoformat()
        redis_client.hset(job_key, "info", json.dumps(job_info))
        redis_client.expire(job_key, 300)
        
        # 从队列中移除
        redis_client.lrem(PRINT_QUEUE, 0, job_id)
        
        # 删除文件
        filepath = job_info.get('filepath')
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"已取消任务 {job_id} 并删除文件")
            
        return jsonify({'success': True, 'message': '任务已取消'}), 200
        
    except Exception as e:
        logger.error(f"取消打印任务失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# 新增：清空所有已完成任务的API
@app.route('/print/jobs/clear_completed', methods=['GET'])
def clear_completed_jobs():
    """清空所有已完成的打印任务（Redis哈希和队列）"""
    try:
        # 获取所有任务ID
        job_keys = redis_client.keys('print_job:*')
        deleted_count = 0
        for key in job_keys:
            job_id = key.decode('utf-8').split(':')[1]
            job_json = redis_client.hget(key, "info")
            if not job_json:
                continue
            job_info = json.loads(job_json.decode('utf-8'))
            if job_info.get('status') not in ['pending', 'printing']:
                # 删除哈希表
                redis_client.delete(key)
                # 从队列移除（防止残留）
                redis_client.lrem(PRINT_QUEUE, 0, job_id)
                deleted_count += 1
        return jsonify({'success': True, 'deleted': deleted_count}), 200
    except Exception as e:
        logger.error(f"清空已完成任务失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    try:
        if opt.debug:
            app.run("0.0.0.0", port=81)
        else:
            waitress.serve(
                app=app,
                host="0.0.0.0",
                port=81,
                threads=2
            )
    except Exception as e:
        print(f"启动失败：{e}")