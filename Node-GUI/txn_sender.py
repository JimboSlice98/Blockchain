import random as rd
import names
import hashlib
import json
import requests
from tqdm import tqdm


def txn_gen(comp_names):
    price = rd.randint(0, 500)

    txn = {'id': '',
           'lender': names.get_full_name(),
           'borrower': names.get_full_name(),
           'type': 'Equity',
           'security': rd.choice(tickers),
           'quantity': rd.randint(0, 100),
           'price': price,
           'strike': price + rd.randint(-20, 20),
           'expiration': f'{rd.randint(2020, 2026)}-{rd.randint(10, 12)}-{rd.randint(10, 28)}',
           'trans_type': 'Origination'}

    # txn = {'id': '',
    #        'origin_id': '8cdb5b0d1c6b0c7f8b7c8ecd9a7098204e372a9b45501e52a8575c8338ceb2bc',
    #        'trigger': 'Expiration',
    #        'trans_type': 'Reversal'}

    txn_str = str(txn['lender']) + str(txn['borrower']) + str(txn['type']) + str(txn['security']) + str(txn['quantity']) + str(txn['price']) + str(txn['strike']) + str(txn['expiration']) + str(txn['trans_type'])
    # txn_str = str(txn['origin_id']) + str(txn['trigger']) + str(txn['trans_type'])

    sha = hashlib.sha256()
    sha.update(txn_str.encode('utf-8'))
    txn['id'] = sha.hexdigest()

    return txn


# my_file = open("comp_names.txt", "r")
# data = my_file.read()
# comp_names = data.split('\n')
# my_file.close()

text_file = open("tickers.txt", "r")
tickers = text_file.read().splitlines()
text_file.close()

for i in tqdm(range(0, 10)):
    txn = txn_gen(tickers)
    print(txn)

    # requests.post('http://146.169.255.177:5000/transaction', json=txn)
    # requests.post('http://155.198.40.43:5000/transaction', json=txn)
    # requests.post('http://155.198.40.49:5000/transaction', json=txn)
    # requests.post('http://155.198.41.51:5000/transaction', json=txn)
