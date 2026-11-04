import requests

BASE_URL = "http://127.0.0.1:5000"

r = requests.get(f"{BASE_URL}/")
print(r.status_code, r.text)

r = requests.post(f"{BASE_URL}/notes", json={"author": "dima", "text": "Классный сайт!"})
print(r.status_code, r.json())

r = requests.post(f"{BASE_URL}/notes", json={"author": "anna", "text": "Всем привет из Казани"})
print(r.status_code, r.json())

r = requests.post(f"{BASE_URL}/notes", json={"author": "dima", "text": "Забыл сказать, Flask работает быстро"})
print(r.status_code, r.json())

r = requests.post(f"{BASE_URL}/notes", json={"author": "dima", "text": "   "})
print(r.status_code, r.json())

r = requests.post(f"{BASE_URL}/notes", json="Просто текст")
print(r.status_code, r.json())

query_params = {"author": "dima", "sort": "id", "order": "desc"}
r = requests.get(f"{BASE_URL}/notes", params=query_params)
print(r.status_code, r.json())

r = requests.get(f"{BASE_URL}/notes", params={"offset": "-5"})
print(r.status_code, r.json())

r = requests.get(f"{BASE_URL}/notes", params={"limit": "500"})
print(r.status_code, r.json())

r = requests.post(f"{BASE_URL}/notes/1/like")
print(r.status_code, r.json())

r = requests.patch(f"{BASE_URL}/notes/2", json={"text": "Всем большой привет из Казани!"})
print(r.status_code, r.json())

r = requests.put(f"{BASE_URL}/notes/3", json={"author": "dima", "text": "Передумал. Django тоже ничего."})
print(r.status_code, r.json())

r = requests.get(f"{BASE_URL}/authors")
print(r.status_code, r.json())

r = requests.get(f"{BASE_URL}/notes/999")
print(r.status_code, r.json())

r = requests.delete(f"{BASE_URL}/notes/2")
print(r.status_code, r.text)

r = requests.delete(f"{BASE_URL}/notes", params={"author": "dima"})
print(r.status_code, r.json())

r = requests.delete(f"{BASE_URL}/notes")
print(r.status_code, r.json())