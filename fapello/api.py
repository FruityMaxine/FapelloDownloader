import requests
from bs4 import BeautifulSoup
from time import sleep

# 用户代理配置，伪装成浏览器
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://fapello.to/"
}

def get_model_info(username_query):
    """
    通过用户名搜索并获取模型详细信息。
    
    参数:
        username_query (str): 搜索关键词
        
    返回:
        dict: 包含 'id', 'name', 'media_count' 的字典, 如果未找到则返回 None
    """
    search_url = f"https://fapello.to/search/{username_query}"
    try:
        # 1. 搜索获取 ID
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        model_id = None
        model_name = None
        
        # 查找搜索结果链接
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if "/model/" in href:
                # 找到第一个匹配的模型链接
                try:
                    parts = href.split("/model/")
                    if len(parts) > 1:
                        temp_id = parts[1].split("/")[0]
                        if temp_id.isdigit():
                            model_id = temp_id
                            # 尝试提取显示的用户名
                            model_name = link.get_text(strip=True)
                            break
                except:
                    continue
        
        if not model_id:
            return None
            
        # 2. 访问模型主页获取媒体统计信息
        profile_url = f"https://fapello.to/model/{model_id}"
        profile_resp = requests.get(profile_url, headers=HEADERS, timeout=10)
        media_count = 0
        
        if profile_resp.status_code == 200:
            p_soup = BeautifulSoup(profile_resp.text, "html.parser")
            try:
                # 使用浏览器工具确认的选择器: 链接包含 /media/ 的 a 标签下的 span.font-bold
                count_el = p_soup.select_one('a[href*="/media/"] span.font-bold')
                if count_el:
                    media_count = int(count_el.get_text(strip=True))
            except:
                pass
                
        # 如果刚才没解析到名字，尝试从Profile页面获取
        if not model_name and profile_resp.status_code == 200:
            try:
               model_name = p_soup.find("h1").get_text(strip=True)
            except:
               model_name = username_query

        return {
            "id": model_id,
            "name": model_name if model_name else username_query,
            "media_count": media_count
        }

    except Exception as e:
        print(f"[异常] 解析用户信息时出错: {e}")
        return None

def get_image_links(model_id, status_callback=None):
    """
    获取指定模型的所有图片原图下载链接。
    """
    page = 1
    all_urls = []
    
    # API 地址模板: https://fapello.to/api/media/{id}/{page}/1/1
    api_template = "https://fapello.to/api/media/{}/{}/1/1"
    
    while True:
        url = api_template.format(model_id, page)
        try:
            if status_callback:
                status_callback(page)
            
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code != 200:
                break
            
            data = response.json()
            
            if not data:
                break
                
            count_in_page = 0
            for item in data:
                # 优先获取 newUrl (原图直链)
                if 'newUrl' in item and item['newUrl']:
                    all_urls.append(item['newUrl'])
                    count_in_page += 1
                elif 'url' in item:
                    all_urls.append(item['url'])
                    count_in_page += 1
            
            if count_in_page == 0 and page > 1:
                break
                
            page += 1
            if page % 10 == 0:
                sleep(0.5)
                
        except Exception as e:
            # 发生异常时停止扫描，返回已找到的
            break
            
    return all_urls
