import requests

# POST请求 = 往服务器发送数据（比如提交表单、新建用户）
url = "https://jsonplaceholder.typicode.com/posts"

# 要发送的数据，就是请求体
body = {
    "title": "我的第一篇文章",
    "body": "这是文章内容",
    "userId": 1
}

response = requests.post(url, json=body)

print("状态码：", response.status_code)
print("返回数据：", response.json())

assert response.status_code == 201, f"状态码错误，期望201，实际{response.status_code}"
print("断言通过，POST请求成功")