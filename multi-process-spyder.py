import os
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import threading

# 参数设置
# 年份
year = 2023
# 月份
month = 6
# 图片保存目录
path = datetime(year, month, 1).strftime('%Y-%m')
save_dir = f"D:/images/{path}/"


# 分析并下载图片
def parse_pic_and_download(year, month, save_dir):
    # 创建图片保存目录
    os.makedirs(save_dir, exist_ok=True)
    # 开始分析
    base_url = "https://www.kindgirls.com"
    # 当月的页面
    date_param = datetime(year, month, 1).strftime('%m-%Y')
    page = f"{base_url}/photo-archive.php?s={date_param}"
    print(f"本月: {date_param}, url: {page}")
    doc = BeautifulSoup(urllib.request.urlopen(page), 'html.parser')
    elements = doc.select(".gal_list  a")

    def download_image(url, save_path):
        try:
            with urllib.request.urlopen(url) as img_url:
                with open(save_path, 'wb') as f:
                    f.write(img_url.read())
            print(f"下载成功: {save_path}")
        except Exception as e:
            print(f"下载失败: {url}, 错误信息: {e}")

    threads = []
    for element in elements:
        href = element['href']
        url = f"{base_url}{href}"
        print(f"图集:{element.text}, url: {url}")
        childdoc = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
        childelements = childdoc.select(".gal_list img")
        for childelement in childelements:
            src = childelement['src']
            print(f"图片: {childelement['title']}, url: {src}", end=" ")
            # 获取图片的URL
            img_url = urllib.request.urlopen(src)
            # 获取图片的文件名
            file_name = os.path.basename(img_url.url)
            # 创建保存图片的文件路径
            save_path = os.path.join(save_dir, file_name)
            thread = threading.Thread(target=download_image, args=(src, save_path))
            thread.start()
            threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print(f"完成：{date_param}, 共下载图片: {len(elements)}张")


# 执行爬虫
parse_pic_and_download(year, month, save_dir)
