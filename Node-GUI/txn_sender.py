import random as rd
import names
import requests
from tqdm import tqdm


def txn_gen(comp_names):
    price = rd.randint(0, 500)

    txn = {'id': rd.randint(100000000, 999999999)}
           # 'lender': names.get_full_name(),
           # 'borrower': names.get_full_name(),
           # 'type': 'equity',
           # 'security': rd.choice(comp_names),
           # 'quantity': rd.randint(0, 100),
           # 'price': price,
           # 'strike': price + rd.randint(-20, 20),
           # 'expiration': f'{rd.randint(2023, 2026)}-{rd.randint(1, 12)}-{rd.randint(1, 31)}'}

    # id = rd.randint(100000000, 999999999)
    # price = rd.randint(0, 500)
    #
    # txn = {f'{id}': {'lender': names.get_full_name(),
    #                  'borrower': names.get_full_name(),
    #                  'type': 'equity',
    #                  'security': rd.choice(comp_names),
    #                  'quantity': rd.randint(0, 100),
    #                  'price': price,
    #                  'strike': price + rd.randint(-20, 20),
    #                  'expiration': f'{rd.randint(2023, 2026)}-{rd.randint(1, 12)}-{rd.randint(1, 31)}'}}

    return txn


my_file = open("comp_names.txt", "r")
data = my_file.read()
comp_names = data.split('\n')
my_file.close()

for i in tqdm(range(100, 101)):
    data = txn_gen(comp_names)
    data['id'] = i
    requests.post('http://155.198.40.39:5000/transaction', json=data)
    requests.post('http://155.198.40.58:5000/transaction', json=data)
    requests.post('http://155.198.40.248:5000/transaction', json=data)
    # requests.post('http://155.198.9.74:5000/transaction', json=data)
    requests.post('http://146.169.253.216:5000/transaction', json=data)

    # print(data)
