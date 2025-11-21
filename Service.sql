/*
 Navicat Premium Dump SQL

 Source Server         : Windows-PDCN
 Source Server Type    : PostgreSQL
 Source Server Version : 180000 (180000)
 Source Host           : 192.168.1.72:5432
 Source Catalog        : Service
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 180000 (180000)
 File Encoding         : 65001

 Date: 21/11/2025 19:30:01
*/


-- ----------------------------
-- Table structure for printer
-- ----------------------------
DROP TABLE IF EXISTS "public"."printer";
CREATE TABLE "public"."printer" (
  "id" int4 NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "location" varchar(255) COLLATE "pg_catalog"."default",
  "type" varchar(255) COLLATE "pg_catalog"."default",
  "status" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for username
-- ----------------------------
DROP TABLE IF EXISTS "public"."username";
CREATE TABLE "public"."username" (
  "id" int8 NOT NULL,
  "usr" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "pwd" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "eml" varchar(255) COLLATE "pg_catalog"."default",
  "phn" varchar(255) COLLATE "pg_catalog"."default",
  "pri" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Primary Key structure for table printer
-- ----------------------------
ALTER TABLE "public"."printer" ADD CONSTRAINT "printer_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table username
-- ----------------------------
ALTER TABLE "public"."username" ADD CONSTRAINT "username_pkey" PRIMARY KEY ("id");
