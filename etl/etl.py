import requests

response = requests.get("https://remotive.com/api/remote-jobs")
data = response.json()
