# MDC-N(ext)G(eneration)

Yet another Movie Data Capture tool

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/mdc-ng/mdc-ng?label=mdc-ng)](https://github.com/mdc-ng/mdc-ng/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/mdcng/mdc?color=orange)](https://hub.docker.com/r/mdcng/mdc/tags)

Telegram发布频道：https://t.me/mdc_ng

## Features

- [x] **智能刮削**：支持30+刮削源，AI人脸识别裁剪，日亚高清海报下载
- [x] **多种整理模式**：硬链接、复制、移动、软链接、原地整理，适配各种场景
- [x] **目录监控**：自动检测新文件并刮削，支持性能和兼容两种模式
- [x] **演员管理**：联动Emby自动刮削演员信息和图片，内置演员数据库
- [x] **手动整理**：可视化文件管理，支持文件扫描、批量操作和任务管理
- [x] **图片增强**：4K/8K、影片类型水印标签，自定义位置和样式
- [x] **智能翻译**：支持OpenAI/Google等多引擎翻译，内置中文标题数据库
- [x] **现代界面**：Web管理界面，支持登录认证、主题切换、NSFW模式

## 技术栈

**后端**：Rust - 高性能、内存安全的系统级语言，零成本抽象实现极轻量内存资源占用

**前端**：Next.js - 现代化React框架，优秀的用户体验

**数据库**：SQLite - 轻量级嵌入式数据库，零配置，易维护

**技术优势**：
- 🚀 **高性能**：Rust原生性能，多线程并发处理，刮削速度快
- 🛡️ **稳定可靠**：内存安全，无垃圾回收停顿，长时间稳定运行
- 🎨 **现代界面**：Next.js响应式设计，支持移动端，交互流畅
- 📦 **部署简单**：编译后单文件部署，Docker一键启动，无复杂依赖
- 🪶 **轻量化**：镜像<300MB，内存占用<300MB，版本更新仅需~60MB

## 功能介绍

### 🎬 视频刮削整理

支持5种整理模式，适配不同存储场景：
- **硬链接模式**：节省空间，推荐本地使用
- **复制/移动模式**：适合跨盘或网盘场景  
- **软链接模式**：创建链接到目标目录
- **原地整理模式**：在原目录生成元数据

**刮削流程**：自动识别番号 → 多源抓取元数据 → 下载处理图片 → 整理文件 → 生成NFO

**字幕支持**：自动整理视频自带字幕文件，支持本地字幕库匹配

### 📁 目录监控

- **性能模式**：实时监听文件变更，适合本地存储
- **兼容模式**：定时检查更新，兼容网盘挂载

支持配置覆盖、文件过滤、自动清理等增强功能

### 👥 演员刮削  

- 联动Emby服务端，自动刮削演员信息和图片
- 数据源：维基百科、minnano-av、graphis、gfriends
- 支持后台新入库演员自动刮削和批量管理

### 🖼️ 图片处理

- **AI裁剪**：人脸识别智能定位裁剪海报
- **日亚高清**：从Amazon日本搜索下载高清海报  
- **水印功能**：4K/8K、影片类型标签，多样式可选
- **独立工具**：专门的海报裁剪工具

### 📊 任务管理与记录

- **任务持久化**：完整的手动任务和监控刮削记录，支持状态追踪，便于维护和分析刮削成果
- **维护操作**：支持批量重试、停止、删除等任务管理功能；支持指定番号或网页进行刮削
- **详情页面**：美观的刮削详情页，包含画廊展示、完整元数据分析和实时日志推送；支持多来源数据手动精选修正
- **日志分析**：详细的刮削日志和错误信息，便于问题排查

### 🌐 数据源支持

覆盖各类视频类型的30+刮削源，支持优先级配置、防反爬、自动重试

## 部署

镜像版本可以去本项目[dockerhub页面](https://hub.docker.com/r/mdcng/mdc)查看

### docker-compose

```yaml
---
version: "2.1"
services:
  mdc:
    image: mdcng/mdc:latest
    container_name: mdc
    environment:
      - PGID=1000 # 可选，设置组ID
      - PUID=1000 # 可选，设置用户ID
      - MDC_USERNAME=admin # 用户名密码可选，配置后开启登录鉴权模块
      - MDC_PASSWORD=admin 
    volumes:
      - /path/to/data:/config # 配置目录，必须
      - /path/to/media:/media # 媒体库，可映射多个
    ports:
      - 9208:9208
    restart: unless-stopped
```

## 支持一下

你可以送我一杯咖啡，以表示对这个项目的支持😉

<img src="https://user-images.githubusercontent.com/124132602/222636597-f8d48940-a528-41e8-9362-8d15f7517bf6.png" width="300" />
