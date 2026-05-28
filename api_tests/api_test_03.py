import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_user():
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] != ""

def test_create_post():
    body = {"title": "测试文章", "body": "内容", "userId": 1}
    response = requests.post(f"{BASE_URL}/posts", json=body)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试文章"
    assert "id" in data

def test_get_not_found():
    response = requests.get(f"{BASE_URL}/users/9999")
    assert response.status_code == 404