import pytest
import requests

def test_get_user(api_base_url):
    response = requests.get(f"{api_base_url}/users/1")
    assert response.status_code == 200
    assert response.json()["name"] != ""
    print("✅ GET用户 通过")

@pytest.mark.parametrize("user_id,expected_status", [
    (1, 200),
    (2, 200),
    (9999, 404),
])
def test_get_users_parametrize(api_base_url, user_id, expected_status):
    response = requests.get(f"{api_base_url}/users/{user_id}")
    assert response.status_code == expected_status
    print(f"✅ 用户{user_id} 状态码{expected_status} 通过")