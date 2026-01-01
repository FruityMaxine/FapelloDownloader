import os
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Downloader:
    def __init__(self, output_dir, max_workers=20):
        """
        初始化下载器。
        
        参数:
            output_dir (str): 图片保存目录
            max_workers (int): 最大并发线程数
        """
        self.output_dir = output_dir
        self.max_workers = max_workers
        self.session = self._create_session()
        
    def _create_session(self):
        """创建带有重试机制的 HTTP 会话"""
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://fapello.to/"
        })
        return session

    def ensure_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def download_image(self, url, progress_callback=None):
        """
        下载单张图片。
        
        参数:
            url (str): 图片 URL
            progress_callback (function): 可选的回调函数，用于 UI 进度更新
        """
        filename = url.split('/')[-1]
        filepath = os.path.join(self.output_dir, filename)

        # 如果文件已存在，跳过
        if os.path.exists(filepath):
            if progress_callback:
                progress_callback(1)
            return

        try:
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            else:
                # 可以选择记录错误日志
                pass
        except Exception as e:
            # 可以选择记录异常
            pass
        finally:
            if progress_callback:
                progress_callback(1)

    def download_all(self, urls, progress_task_id, progress_object):
        """
        批量并发下载。
        
        参数:
            urls (list): 图片 URL 列表
            progress_task_id: Rich 进度条的任务 ID
            progress_object: Rich 进度条对象，用于直接调用 update
        """
        self.ensure_dir()
        
        def callback(completed_count):
            progress_object.update(progress_task_id, advance=completed_count)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            futures = [executor.submit(self.download_image, url, callback) for url in urls]
            # 等待所有任务完成
            for future in futures:
                future.result()
