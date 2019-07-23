import requests
import json

payload = {
    'id': "000UC010000006189",
    'env': 'sit2',
}


r = requests.request('get', "http://127.0.0.1:8000/data/migration/merchant/", params=payload)
print(r.json())

