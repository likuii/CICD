import feedparser

# 读取 RSS feed
rss_url = "https://rsshub.moeyy.cn/weibo/search/hot"
feed = feedparser.parse(rss_url)

print("###############Start####################")
# 创建 README.md 文件并写入数据
with open("WeiBo.md", "w", encoding="utf-8") as f:
    # 写入标题和链接
    f.write(f"# {feed['channel']['title']}\n\n")
    f.write(f"本文链接: {feed['channel']['link']}\n\n")

    # 遍历所有 item 并写入标题、描述、链接和唯一标识符 GUID
    for idx, item in enumerate(feed["items"]):
        f.write(f"## 文章 {idx+1}\n")
        f.write(f"- 标题: {item['title']}\n")
        f.write(f"- 描述: {item['description']}\n")
        f.write(f"- 链接: {item['link']}\n")
        f.write(f"- 唯一标识符GUID: {item['guid']}\n\n")
print("###############End####################")