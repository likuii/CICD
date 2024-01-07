import urllib.request
import xml.etree.ElementTree as ET

# 获取RSS Feed内容
url = 'https://rsshub.moeyy.cn/bing'

try:
    response = urllib.request.urlopen(url)
except urllib.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")

xml_str = response.read().decode('utf-8')

# 解析XML并获取数据
root = ET.fromstring(xml_str)

# 生成Markdown格式的文本
md_text = f'# {root.find("./channel/title").text}\n\n'
md_text += f'[{root.find("./channel/link").text}]({root.find("./channel/link").text})\n\n'
md_text += f'{root.find("./channel/description").text}\n\n'
for item in root.findall('./channel/item'):
    title = item.find('title').text
    link = item.find('link').text
    description = item.find('description').text
    img_url = description.split('src="')[1].split('"')[0]
    md_text += f'## {title}\n\n'
    md_text += f'![{title}]({img_url})\n\n'
    md_text += f'[查看原图]({link})\n\n'

# 写入README.md文件
with open('Bing.md', 'w', encoding='utf-8') as f:
    f.write(md_text)

print('已将图片添加到Bing.md文件')
