import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "exchange_rate/aave/usd/100")
print(response.json())

