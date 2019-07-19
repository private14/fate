import requests
import json

payload = {
    'id': "000UC010000006189",
    'env': 'sit2',
}


r = requests.request('get', "http://127.0.0.1:8000/data/migration/merchant/", params=payload)
print(r.json())



{"acct": {"host": "192.168.0.210", "port": "3306", "user": "sit1", "password": "sit2019!", "database": "acct"}, "channel": {"host": "192.168.0.210", "port": "3306", "user": "sit1", "password": "sit2019!", "database": "channel"}, "credittrans": {"host": "192.168.0.210", "port": "3306", "user": "sit1", "password": "sit2019!", "database": "credittrans"}, "loanuser": {"host": "192.168.0.210", "port": "3306", "user": "sit1", "password": "sit2019!", "database": "loanuser"},"product": {"host": "192.168.0.210", "port": "3306", "user": "sit1", "password": "sit2019!", "database": "product"}}
{"acct": {"host": "192.168.0.211", "port": "3306", "user": "sit2", "password": "sit2019@", "database": "acct"}, "channel": {"host": "192.168.0.211", "port": "3306", "user": "sit2", "password": "sit2019@", "database": "channel"}, "credittrans": {"host": "192.168.0.211", "port": "3306", "user": "sit2", "password": "sit2019@", "database": "credittrans"}, "loanuser": {"host": "192.168.0.211", "port": "3306", "user": "sit2", "password": "sit2019@", "database": "loanuser"}, "product": {"host": "192.168.0.211", "port": "3306", "user": "sit2", "password": "sit2019@", "database": "product"}}