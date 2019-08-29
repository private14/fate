import requests

# payload = {
#     'id': "PN00004004-0001",
#     'env': 'sit1',
#     'source': 'sit2'
# }
#
#
# r = requests.request('get', "http://127.0.0.1:8000/data/migration/merchant/", params=payload)
# print(r.json())


r = requests.request('get', "http://127.0.0.1:8000/common/random/")
print(r.json())
