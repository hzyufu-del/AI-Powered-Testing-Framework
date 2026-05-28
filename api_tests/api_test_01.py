import requests

url = "https://jsonplaceholder.typicode.com/users/1"
response = requests.get(url)

data = response.json()

# 断言状态码
assert response.status_code == 200, f"状态码错误：{response.status_code}"

# 取出具体字段
print("用户名：", data["name"])
print("邮箱：", data["email"])
print("城市：", data["address"]["city"])

# 断言字段不为空
assert data["name"] != "", "name字段为空！"
print("断言通过，接口返回数据正常")