import requests

payload = {
    'id': "PN00004023-0003",
    'env': 'sit3',
}


r = requests.request('get', "http://127.0.0.1:8000/data/migration/merchant/", params=payload)
print(r.json())

