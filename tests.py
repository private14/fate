import requests

payload = {
    'id': "PN00000039-0001",
    'env': 'sit2',
}


r = requests.request('get', "http://127.0.0.1:8000/data/migration/merchant/", params=payload)
print(r.json())

