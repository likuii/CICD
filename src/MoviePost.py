import xml.etree.ElementTree as ET
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import random

# 获取RSS源
url = 'https://rsshub.moeyy.cn/douban/movie/playing'
response = requests.get(url)
data = response.content

# 解析XML
root = ET.fromstring(data)

# 遍历每个电影条目并提取信息
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

# 设置字体  拷贝设置
font_title = ImageFont.truetype('/usr/share/fonts/truetype/liberation/msyh.ttf', 36)
font_subtitle = ImageFont.truetype('/usr/share/fonts/truetype/liberation/msyh.ttf', 24)
font_text = ImageFont.truetype('/usr/share/fonts/truetype/liberation/msyh.ttf', 18)

# 随机抽取9个电影并生成九宫格图片
selected_movies = random.sample(movies, 9)
grid_size = (1020, 1020)  # 图片大小
padding = 10  # 图片之间的间距
bg_color = (255, 255, 255)  # 背景颜色
grid_image = Image.new('RGB', grid_size, bg_color)
image_size = (300, 300)  # 每张图片的大小
# 计算出总共需要留白的像素数，注意这里要用到浮点数除法
total_padding_width = (grid_size[0] - image_size[0] * 3) / 2
total_padding_height = (grid_size[1] - image_size[1] * 3) / 2

# 根据计算出的留白像素数调整 positions 中的坐标
positions = [(int(j*(image_size[0]+padding)+total_padding_width),
              int(i*(image_size[1]+padding)+total_padding_height))
             for i in range(3) for j in range(3)]
for i, movie in enumerate(selected_movies):
    try:
        response = requests.get(movie['image_url'])
        img = Image.open(io.BytesIO(response.content))
        img.thumbnail(image_size)
        position = positions[i]
        grid_image.paste(img, position)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        break

# 保存九宫格图片
grid_filename = 'Image/movies_grid.png'
grid_image.save(grid_filename)

# 将九宫格图片插入Markdown文件
with open('Movie.md', 'a',encoding='utf-8') as f:
    f.write('\n\n')
    f.write('## 随机抽取的9部电影\n\n')
    f.write('<img src="{}" alt="movie posters">\n'.format(grid_filename))

# 生成每个电影的信息图片并保存
for i, movie in enumerate(movies):
    if movie not in selected_movies:
        continue
    try:
        response = requests.get(movie['image_url'])
        img = Image.open(io.BytesIO(response.content))
        canvas_width = 800
        canvas_height = 700
        canvas_bg_color = (255, 255, 255)
        canvas = Image.new('RGB', (canvas_width, canvas_height), canvas_bg_color)
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 20), movie['title'], font=font_title, fill=(0, 0, 0))
        draw.text((20, 70), f"评分：{movie['rating']}", font=font_subtitle, fill=(0, 0, 0))
        draw.text((20, 110), f"片长：{movie['runtime']}", font=font_subtitle, fill=(0, 0, 0))
        draw.text((20, 150), f"制片国家/地区：{movie['country']}", font=font_subtitle, fill=(0, 0, 0))
        draw.text((20, 190), f"导演：{movie['director']}", font=font_subtitle, fill=(0, 0, 0))
        draw.text((20, 230), f"主演：{movie['cast']}", font=font_subtitle, fill=(0, 0, 0))
        canvas.paste(img, (20, 280))
        filename = f"Image/movie-{i + 1}.png"
        canvas.save(filename)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        break

# 在Markdown文件中插入每个电影的信息图片
with open('Movie.md', 'a',encoding='utf-8') as f:
    for i, movie in enumerate(selected_movies):
        image_filename = f"Image/movie-{i+1}.png"
        f.write('\n\n')
        f.write(f'### {movie["title"]}\n\n')
        f.write(f'<img src="{image_filename}" alt="{movie["title"]}">\n')
        f.write(f'评分：{movie["rating"]}\n\n')
        f.write(f'片长：{movie["runtime"]}\n\n')
        f.write(f'制片国家/地区：{movie["country"]}\n\n')
        f.write(f'导演：{movie["director"]}\n\n')
        f.write(f'主演：{movie["cast"]}\n\n')

print("Done")
