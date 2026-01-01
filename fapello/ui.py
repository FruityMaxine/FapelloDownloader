from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from .api import get_model_info, get_image_links
from .downloader import Downloader
import os
import questionary
import re

console = Console()

# 语言包字典
LANG = {
    "zh": {
        "banner_title": "Fapello 下载器",
        "banner_subtitle": "基于 Python 的高效多线程下载工具",
        "select_lang": "请选择语言 / Please select language:",
        "input_user": "请输入目标用户名",
        "searching": "正在搜索用户 '{}' ...",
        "error_not_found": "错误: 未能找到用户 '{}'。",
        "found_title": "找到目标用户",
        "user_label": "用户名",
        "id_label": "用户ID",
        "count_label": "预计媒体数",
        "confirm_msg": "是否确认为此用户并开始扫描?",
        "cancel_msg": "操作已取消。",
        "scan_start": "正在扫描 API 获取图片链接...",
        "scan_desc": "扫描页面",
        "scan_page": "{} 页",
        "error_no_links": "错误: 未找到任何图片链接。",
        "scan_complete": "扫描完成! 共发现 {} 张图片。",
        "path_msg": "准备下载到: {}",
        "download_desc": "正在下载...",
        "complete_msg": "全部完成! 文件已保存至: {}"
    },
    "en": {
        "banner_title": "Fapello Downloader",
        "banner_subtitle": "Efficient Multi-threaded Downloader",
        "select_lang": "Please select language:",
        "input_user": "Enter target username",
        "searching": "Searching for user '{}' ...",
        "error_not_found": "Error: User '{}' not found.",
        "found_title": "Target User Found",
        "user_label": "Username",
        "id_label": "User ID",
        "count_label": "Est. Media Count",
        "confirm_msg": "Confirm user and start scanning?",
        "cancel_msg": "Operation cancelled.",
        "scan_start": "Scanning API for image links...",
        "scan_desc": "Scanning Pages",
        "scan_page": "{} Pages",
        "error_no_links": "Error: No image links found.",
        "scan_complete": "Scan Complete! Found {} images.",
        "path_msg": "Downloading to: {}",
        "download_desc": "Downloading...",
        "complete_msg": "All Done! Files saved to: {}"
    }
}

CURRENT_LANG = "zh"

def t(key):
    """获取本地化字符串"""
    return LANG.get(CURRENT_LANG, LANG["zh"]).get(key, key)

def print_banner():
    """打印欢迎横幅"""
    banner = f"""
    [bold magenta]{t('banner_title')}[/bold magenta]
    [cyan]{t('banner_subtitle')}[/cyan]
    """
    console.print(Panel(banner, border_style="magenta"))

def select_language():
    """使用箭头键选择语言"""
    global CURRENT_LANG
    answer = questionary.select(
        "Language / 语言:",
        choices=[
            questionary.Choice("简体中文", value="zh"),
            questionary.Choice("English", value="en")
        ],
        qmark=""
    ).ask()
    if answer:
        CURRENT_LANG = answer

def run_interactive():
    """运行交互式主程序"""
    # 0. 选择语言
    select_language()
    print_banner()
    
    # 1. 获取用户名
    username = questionary.text(f"[{t('input_user')}]", qmark="").ask()
    if not username:
        return
        
    # 2. 解析 ID 和信息
    info = None
    with console.status(f"[bold yellow]{t('searching').format(username)}[/bold yellow]", spinner="dots"):
        info = get_model_info(username)
        
    if not info:
        console.print(f"[bold red]{t('error_not_found').format(username)}[/bold red]")
        return

    model_id = info['id']
    target_name = info['name']
    media_count = info['media_count']

    console.print(Panel(f"""
    [bold cyan]{t('found_title')}[/bold cyan]
    {t('user_label')}: [green]{target_name}[/green]
    {t('id_label')}: [green]{model_id}[/green]
    {t('count_label')}: [green]{media_count}[/green]
    """, border_style="green"))
    
    # 3. 确认是否正确 (使用 questionary)
    confirmed = questionary.confirm(t('confirm_msg'), default=True, qmark="").ask()
    if not confirmed:
        console.print(t('cancel_msg'))
        return

    # 4. 扫描图片链接
    all_urls = []
    # 如果有媒体总数，我们可以估算大致的百分比 (假设每页12个)
    total_pages_est = (media_count // 12) + 1 if media_count else 0
    
    console.print(f"[yellow]{t('scan_start')}[/yellow]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn(t('scan_page').format("{task.completed}")),
        console=console
    ) as scan_progress:
        scan_task = scan_progress.add_task(f"[cyan]{t('scan_desc')}[/cyan]", total=total_pages_est if total_pages_est > 0 else None)
        
        def update_scan_status(page_num):
            scan_progress.update(scan_task, completed=page_num)
            
        all_urls = get_image_links(model_id, update_scan_status)
        
    if not all_urls:
        console.print(f"[bold red]{t('error_no_links')}[/bold red]")
        return
        
    console.print(f"[bold green]{t('scan_complete').format(len(all_urls))}[/bold green]")
    
    # 5. 自动设置保存路径 (downloads/username)
    safe_name = re.sub(r'[\\/*?:"<>|]', "", target_name) # 移除非法字符
    output_dir = os.path.join(os.getcwd(), "downloads", safe_name)
    
    console.print(t('path_msg').format(f"[underline]{output_dir}[/underline]"))
    
    # 6. 开始下载
    downloader = Downloader(output_dir)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task_id = progress.add_task(f"[cyan]{t('download_desc')}[/cyan]", total=len(all_urls))
        downloader.download_all(all_urls, task_id, progress)
        
    console.print(f"[bold green]{t('complete_msg').format(output_dir)}[/bold green]")
