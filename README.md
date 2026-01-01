# Fapello Downloader / Fapello 下载器

[English](#english) | [简体中文](#简体中文)

---

<a name="english"></a>
## 🇬🇧 English

A professional, modular, and efficient Python command-line tool to download images from [Fapello](https://fapello.to/). It features automatic user ID resolution, multi-threaded downloading, and a beautiful terminal UI.

### ✨ Features

- **Auto ID Resolution**: No need to manually find the model ID. Just enter the username (e.g., `tenletters`), and the tool will resolve it automatically.
- **Accurate Media Count**: Precisely extracts the total media count from the profile page.
- **Fast Downloading**: Uses multi-threading to download images concurrently for maximum speed.
- **Modern UI**: Built with `Rich` and `Questionary`, providing a clean, emoji-free, and interactive terminal interface with progress bars.
- **Multi-language Support**: Select between **Simplified Chinese** and **English** at startup.

### 📦 Installation

1. Ensure you have Python 3.8+ installed.
2. Clone this repository.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 🚀 Usage

Run the main script:

```bash
python main.py
```

Follow the interactive prompts:
1. Select your language (Use arrow keys).
2. Enter the target username.
3. Confirm the found user and media count.
4. Watch it automatically scan and download!

### 🛠️ Project Structure

```text
FapelloDownloader/
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── fapello/           # Core package
    ├── api.py         # API interaction logic
    ├── downloader.py  # Multi-threaded downloader
    └── ui.py          # Terminal UI
```

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

一个专业、模块化且高效的 Python 命令行工具，用于从 [Fapello](https://fapello.to/) 下载图片。支持自动解析用户 ID、多线程下载以及漂亮的终端界面。

### ✨ 功能特点

- **自动 ID 解析**: 无需手动查找数字 ID，只需输入用户名（例如 `tenletters`），程序会自动解析。
- **精准媒体计数**: 能够从个人主页精准提取媒体总数，不再显示为 0。
- **极速下载**: 使用多线程并发下载，最大化网络利用率。
- **现代化界面**: 基于 `Rich` 和 `Questionary` 构建，提供干净（无多余 Emoji）、交互式的终端 UI，包含实时进度条。
- **多语言支持**: 启动时可选择 **简体中文** 或 **English**。

### 📦 安装

1. 确保已安装 Python 3.8+。
2. 克隆本项目。
3. 安装依赖：

```bash
pip install -r requirements.txt
```

### 🚀 使用方法

直接运行主程序：

```bash
python main.py
```

按照屏幕提示操作：
1. 使用键盘方向键选择语言。
2. 输入目标用户名。
3. 确认找到的用户及媒体数量。
4. 程序将自动开始扫描并下载！

### 🛠️ 项目结构

```text
FapelloDownloader/
├── main.py            # 程序入口
├── requirements.txt   # 项目依赖
└── fapello/           # 核心模块包
    ├── api.py         # 网站 API 交互逻辑
    ├── downloader.py  # 多线程下载逻辑
    └── ui.py          # 终端用户界面
```

### 📝 Disclaimer / 免责声明

This tool is for educational purposes and personal backup only. Please do not use it for malicious scraping or DDOS attacks. / 本工具仅供学习和个人备份使用。请勿高频恶意请求，以免被封禁 IP。
