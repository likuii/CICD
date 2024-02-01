import xml.etree.ElementTree as ET
import requests

# 获取RSS源


print("###############StartMovie####################")
url = 'https://rsshub.moeyy.cn/douban/movie/playing'
response = requests.get(url)
data = response.content

# 解析XML
root = ET.fromstring(data)

# 遍历每个电影条目并提取信息
movies = []
for item in root.findall('./channel/item'):
    title = item.find('title').text.strip()  # 标题
    rating = item.find('description').text.split('<br>')[1].split('：')[1]  # 评分
    runtime = item.find('description').text.split('<br>')[2].split('：')[1]  # 片长
    country = item.find('description').text.split('<br>')[3].split('：')[1]  # 制片国家/地区
    director = item.find('description').text.split('<br>')[4].split('：')[1]  # 导演
    cast = item.find('description').text.split('<br>')[5].split('：')[1]  # 主演
    image_url = item.find('description').text.split('<img src="')[1].split('" ')[0]  # 海报图片链接

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

# 将电影列表保存为README.md文件
with open('EDITREADME.md', mode='w', encoding='utf-8') as f:
    f.write('# Douban Currently Playing Movies\n\n')
    for movie in movies:
        f.write(f'## {movie["title"]}\n')
        f.write(f'**Rating:** {movie["rating"]}\n')
        f.write(f'**Runtime:** {movie["runtime"]}\n')
        f.write(f'**Country:** {movie["country"]}\n')
        f.write(f'**Director:** {movie["director"]}\n')
        f.write(f'**Cast:** {movie["cast"]}\n')
        # 保证导出来的图片靠左边对齐
        f.write(f'<div align="left">\n<img src="{movie["image_url"]}" alt="{movie["title"]}">\n</div>\n')
        f.write('\n---\n')

print("###############EndMovie####################")