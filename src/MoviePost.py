import xml.etree.ElementTree as ET
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# 获取RSS源
url = 'http://rsshub.baitry.com/douban/movie/playing'
response = requests.get(url)
data = response.content

# 解析XML
root = ET.fromstring(data)

# 遍历每个电影条目并提取信息

print("数据处理开始")
movies = []
for item in root.findall('./channel/item'):
    title = item.find('title').text.strip()
    rating = item.find('description').text.split('<br>')[1].split('：')[1]
    runtime = item.find('description').text.split('<br>')[2].split('：')[1]
    country = item.find('description').text.split('<br>')[3].split('：')[1]
    director = item.find('description').text.split('<br>')[4].split('：')[1]
    cast = item.find('description').text.split('<br>')[5].split('：')[1]
    image_url = item.find('description').text.split('<img src="')[1].split('" ')[0]

    # 将提取的信息添加到电影列表
    movie = {
        'title': title,
        'rating': rating,
        'runtime': runtime,
        'country': country,
        'director': director,
        'cast': cast,
        'image_url': image_url
    }
    movies.append(movie)

# 设置字体
font_title = ImageFont.truetype('/Font/msyh/msyh.ttc', 36)
font_subtitle = ImageFont.truetype('/Font/msyh/msyh.ttc', 24)
font_text = ImageFont.truetype('/Font/msyh/msyh.ttc', 18)

# 生成电影信息图片并保存
for i, movie in enumerate(movies):
    # 打开海报图片
    response = requests.get(movie['image_url'])
    img = Image.open(io.BytesIO(response.content))

    # 创建画布
    canvas_width = 800
    canvas_height = 700
    canvas_bg_color = (255, 255, 255)
    canvas = Image.new('RGB', (canvas_width, canvas_height), canvas_bg_color)

    # 在画布上绘制电影信息
    draw = ImageDraw.Draw(canvas)
    draw.text((20, 20), movie['title'], font=font_title, fill=(0, 0, 0))
    draw.text((20, 70), f"评分：{movie['rating']}", font=font_subtitle, fill=(0, 0, 0))
    draw.text((20, 110), f"片长：{movie['runtime']}", font=font_subtitle, fill=(0, 0, 0))
    draw.text((20, 150), f"制片国家/地区：{movie['country']}", font=font_subtitle, fill=(0, 0, 0))
    draw.text((20, 190), f"导演：{movie['director']}", font=font_subtitle, fill=(0, 0, 0))
    draw.text((20, 230), f"主演：{movie['cast']}", font=font_subtitle, fill=(0, 0, 0))
    canvas.paste(img, (20, 280))

    print("Running")
    # 将图片保存到文件
    filename = f"Image/movie-{i+1}.png"
    canvas.save(filename)
    print("End")

