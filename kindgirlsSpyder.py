import os
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

# 参数设置
# 年份
year = 2023
# 月份
month = 7
# 图片保存目录



# 分析并下载图片
def parse_pic_and_download(year, month, save_dir):
    # 创建图片保存目录
    os.makedirs(save_dir, exist_ok=True)
    # 开始分析
    base_url = "https://www.kindgirls.com"
    # 当月的页面
    date_param = datetime(year, month, 1).strftime('%m-%Y')
    page = f"{base_url}?s={date_param}"
    print(f"本月: {date_param}, url: {page}")
    doc = BeautifulSoup(urllib.request.urlopen(page), 'html.parser')
    elements = doc.select(".bloque  a")
    count = 0
    for element in elements:
        href = element['href']
        url = f"{base_url}{href}"
        print(f"图集:{element.text}, url: {url}")
        childdoc = BeautifulSoup(urllib.request.urlopen(url), 'html.parser')
        childelements = childdoc.select(".gal_list img")
        for childelement in childelements:
            src = childelement['src']
            print(f"图片{count + 1}: {childelement['title']}, url: {src}", end=" ")
            # 获取图片的URL
            img_url = urllib.request.urlopen(src)
            # 获取图片的文件名
            file_name = os.path.basename(img_url.url)
            # 创建保存图片的文件路径
            save_path = os.path.join(save_dir, file_name)
            # 下载图片并保存到指定目录
            with open(save_path, 'wb') as f:
                f.write(img_url.read())
            print(f"下载到: {save_path}")
            count += 1
    print(f"完成：{date_param}, 共下载图片: {count}张")


# 执行爬虫
for i in range(2011,2023):
    for j in range(1,13):
        year = i
        month = j
        path = datetime(year, month, 1).strftime('%Y-%m')
        save_dir = f"/home/zhechen/Downloads/ImageAssistant_Batch_Image_Downloader/imgs/{path}/"
        parse_pic_and_download(year, month, save_dir)
