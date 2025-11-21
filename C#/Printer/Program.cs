using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Printing;
using System.IO;
using System.Linq;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace Printer
{
    public class PrintConfig
    {
        public int Id { get; set; }
        public string Printer { get; set; }
        public string File { get; set; }
        public string Filetype { get; set; }
        public int Copies { get; set; }
        public int Duplex { get; set; }
        public string Route { get; set; }
        public int Pagenum { get; set; }
    }

    internal class Program
    {
        private static int _id = 0;
        private static string _printerName = string.Empty;
        private static int _copies = 1;
        private static bool _duplex = false;
        private static bool _rotate = false;
        private static List<Image> _imagesToPrint = new List<Image>();

        // 当前正在打印的图片索引
        private static int _currentImageIndex = 0;

        static void Main(string[] args)
        {
            try
            {
                string yamlFilePath = ParseCommandLineArgs(args);

                if (!string.IsNullOrEmpty(yamlFilePath))
                {
                    Console.WriteLine($"找到 YAML 配置文件: {yamlFilePath}");
                    ProcessYamlPrintJob(yamlFilePath);
                }
                else
                {
                    Console.WriteLine("未提供有效的 YAML 配置文件。");
                    Console.WriteLine("用法: Printer.exe --yaml <path_to_your_config.yaml>");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"发生错误: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
            finally
            {
                foreach (var img in _imagesToPrint)
                {
                    img.Dispose();
                }
            }
        }

        private static string ParseCommandLineArgs(string[] args)
        {
            for (int i = 0; i < args.Length; i++)
            {
                if (args[i].Equals("--yaml", StringComparison.OrdinalIgnoreCase) && i + 1 < args.Length)
                {
                    return args[i + 1];
                }
            }
            return null;
        }

        private static void ProcessYamlPrintJob(string yamlFilePath)
        {
            if (!File.Exists(yamlFilePath))
            {
                throw new FileNotFoundException("YAML 配置文件未找到", yamlFilePath);
            }

            string yamlContent = File.ReadAllText(yamlFilePath);

            var deserializer = new DeserializerBuilder()
                .WithNamingConvention(CamelCaseNamingConvention.Instance)
                .Build();
            PrintConfig config = deserializer.Deserialize<PrintConfig>(yamlContent);

            _printerName = config.Printer;
            _copies = config.Copies;
            _duplex = config.Duplex == 1;
            _rotate = config.Route.Equals("v", StringComparison.OrdinalIgnoreCase);
            _id = config.Id;

            string taskDirectory = Path.GetDirectoryName(yamlFilePath);
            string frontDir = Path.Combine(taskDirectory, _id.ToString(), "Front");
            string backDir = Path.Combine(taskDirectory, _id.ToString(), "Back");

            Console.WriteLine("开始加载图片...");
            LoadImagesFromDirectory(frontDir);
            if (_duplex) // 如果存在双面的话，我们再分双面打印
            {
                LoadImagesFromDirectory(backDir);
            }
            
            Console.WriteLine($"图片加载完成，共 {_imagesToPrint.Count} 页。");

            if (_imagesToPrint.Count == 0)
            {
                Console.WriteLine("警告：未找到任何可打印的图片。");
                return;
            }

            PrintAllImages();

            Console.WriteLine("打印任务已提交，开始清理临时文件...");
            CleanupTempFiles(taskDirectory, yamlFilePath, frontDir, backDir);
            Console.WriteLine("临时文件清理完毕。");
        }

        private static void LoadImagesFromDirectory(string directoryPath)
        {
            if (!Directory.Exists(directoryPath))
            {
                Console.WriteLine($"警告：目录不存在，跳过加载: {directoryPath}");
                return;
            }

            var imageFiles = Directory.EnumerateFiles(directoryPath, "*.png")
                                      .OrderBy(f => Path.GetFileName(f))
                                      .ToList();

            foreach (var file in imageFiles)
            {
                try
                {
                    // 使用 FileStream 以只读方式打开，并提示 Image 从流中读取，这样可以在加载后删除文件
                    using (var stream = new FileStream(file, FileMode.Open, FileAccess.Read))
                    {
                        Image img = Image.FromStream(stream);
                        _imagesToPrint.Add(img);
                    }
                    Console.WriteLine($"已加载图片: {file}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"加载图片 {file} 失败: {ex.Message}");
                }
            }
        }

        private static void PrintAllImages()
        {
            using (PrintDocument pd = new PrintDocument())
            {
                pd.PrinterSettings.PrinterName = _printerName;
                pd.PrinterSettings.Copies = (short)_copies;
                pd.PrinterSettings.Duplex = _duplex ? Duplex.Vertical : Duplex.Simplex;

                pd.DefaultPageSettings.Margins = new Margins(0, 0, 0, 0); // 页边距设置为 0

                pd.PrintPage += Pd_PrintPage;

                Console.WriteLine($"开始向打印机 '{_printerName}' 提交任务...");
                Console.WriteLine($"配置: 份数={_copies}, 双面={(pd.PrinterSettings.Duplex == Duplex.Vertical ? "是" : "否")}, 旋转={(_rotate ? "是" : "否")}");
                pd.Print();
                Console.WriteLine("打印任务已成功提交。");
            }
        }

        private static void Pd_PrintPage(object sender, PrintPageEventArgs e)
        {
            if (_currentImageIndex >= _imagesToPrint.Count)
            {
                e.HasMorePages = false;
                _currentImageIndex = 0;
                return;
            }

            Image currentImage = _imagesToPrint[_currentImageIndex];
            Image imageToPrint = currentImage;

            Console.WriteLine($"正在打印第 {_currentImageIndex + 1}/{_imagesToPrint.Count} 页...");

            if (_rotate)
            {
                imageToPrint = new Bitmap(currentImage);
                imageToPrint.RotateFlip(RotateFlipType.Rotate90FlipNone);
            }

            float scale = Math.Min(e.MarginBounds.Width / (float)imageToPrint.Width, e.MarginBounds.Height / (float)imageToPrint.Height);
            int newWidth = (int)(imageToPrint.Width * scale);
            int newHeight = (int)(imageToPrint.Height * scale);
            int x = e.MarginBounds.Left + (e.MarginBounds.Width - newWidth) / 2;
            int y = e.MarginBounds.Top + (e.MarginBounds.Height - newHeight) / 2;

            e.Graphics.SmoothingMode = SmoothingMode.AntiAlias;
            e.Graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
            e.Graphics.DrawImage(imageToPrint, x, y, newWidth, newHeight);

            if (imageToPrint != currentImage)
            {
                imageToPrint.Dispose();
            }

            _currentImageIndex++;
            e.HasMorePages = _currentImageIndex < _imagesToPrint.Count;
        }

        private static void CleanupTempFiles(string taskDirectory, string yamlFilePath, string frontDir, string backDir)
        {
            try
            {
                if (File.Exists(yamlFilePath)) File.Delete(yamlFilePath);
                if (Directory.Exists(frontDir)) Directory.Delete(frontDir, recursive: true);
                if (Directory.Exists(backDir)) Directory.Delete(backDir, recursive: true);
                if (Directory.Exists(taskDirectory) && Directory.GetFileSystemEntries(taskDirectory).Length == 0)
                {
                    Directory.Delete(taskDirectory);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"清理临时文件时发生错误: {ex.Message}。请手动检查并删除。");
            }
        }
    }
}