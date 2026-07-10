import requests

# Test Login
login_url = "http://127.0.0.1:8000/api/v1/identity/auth/login/"
data = {
    "email": "admin@example.com",
    "password": "admin"
}

print(f"POST {login_url}")
response = requests.post(login_url, json=data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    token = response.json().get('access')
    print("Token received!")
    
    # Test Get Users
    users_url = "http://127.0.0.1:8000/api/v1/identity/users/"
    headers = {"Authorization": f"Bearer {token}"}
    print(f"\nGET {users_url}")
    user_resp = requests.get(users_url, headers=headers)
    print(f"Status: {user_resp.status_code}")
    print(user_resp.json())
else:
    print(response.json())
