import random as rd
import names
import hashlib
import json
import requests
from tqdm import tqdm


def txn_gen(comp_names):
    price = rd.randint(0, 500)

    txn = {'id': '',
           'lender': 'Jamie',#names.get_full_name(),
           'borrower': names.get_full_name()}
           # 'type': 'equity',
           # 'security': rd.choice(comp_names),
           # 'quantity': rd.randint(0, 100),
           # 'price': price,
           # 'strike': price + rd.randint(-20, 20),
           # 'expiration': f'{rd.randint(2023, 2026)}-{rd.randint(1, 12)}-{rd.randint(1, 31)}'}

    txn_str = str(txn['lender']) + str(txn['borrower'])# + str(txn['type']) + str(txn['security']) + str(txn['quantity']) + str(txn['price']) + str(txn['strike']) + str(txn['expiration'])

    sha = hashlib.sha256()
    sha.update(txn_str.encode('utf-8'))
    txn['id'] = sha.hexdigest()

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


# Function to compute the combines value of two hashes
def hash2(hash_a, hash_b):
    # Reverse inputs before and after hashing due to big-endian / little-endian nonsense
    combinedHash = hash_a[::-1] + hash_b[::-1]

    sha = hashlib.sha256()
    sha.update(combinedHash.encode('utf-8'))
    hash = sha.hexdigest()

    return hash


# Function to hash a pair of items recursively to find the Merkle root
def merkle(hashList):
    if len(hashList) == 1:
        return hashList[0]

    newHashList = []
    # Create hash of pairs of values, for odd length the last is skipped
    for i in range(0, len(hashList) - 1, 2):
        newHashList.append(hash2(hashList[i], hashList[i+1]))

    # Hash the last item twice if the list contains an odd number of items
    if len(hashList) % 2 == 1:
        newHashList.append(hash2(hashList[-1], hashList[-1]))

    return merkle(newHashList)


my_file = open("comp_names.txt", "r")
data = my_file.read()
comp_names = data.split('\n')
my_file.close()

for i in tqdm(range(0, 10)):
    txn = txn_gen(comp_names)
    print(txn)

    requests.post('http://146.169.255.177:5000/transaction', json=txn)
    requests.post('http://155.198.40.43:5000/transaction', json=txn)
    requests.post('http://155.198.40.49:5000/transaction', json=txn)
    requests.post('http://155.198.41.51:5000/transaction', json=txn)
