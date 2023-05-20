text = "Hello, world!"

# 打开文件并写入文本
with open('output.txt', 'w') as f:
    f.write(text)

print("文件已保存")
