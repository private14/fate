import requests

payload = {
    'id': "PN00004004-0001",
    'env': 'sit3',
    'source': 'sit2'
}


#r = requests.request('get', "http://127.0.0.1:8000/data/migration/merchant/", params=payload)
r = requests.request('get', "http://127.0.0.1:8000/swagger/api/env", params=payload)
print(r.json())

