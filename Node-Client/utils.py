from datetime import datetime
import socket
import requests
import database
import os
import shutil
import hashlib

# Import from custom scripts
from config import *
import block
import sync
import transaction as txn


# def dict_from_block_attributes(**kwargs):
#     info = {}
#     for key in kwargs:
#         if key in BLOCK_VAR_CONVERSIONS:
#             info[key] = BLOCK_VAR_CONVERSIONS[key](kwargs[key])
#
#         else:
#             info[key] = kwargs[key]
#
#     return info
#
#
# def create_new_block(prev_block=None, timestamp=None, origin=None, data=None):
#     if not prev_block:
#         # Check the local directory for JSON files
#         for fname in os.listdir(CHAINDATA_DIR):
#             if fname.endswith('.json'):
#                 # Gather last block from local directory
#                 prev_block = sync.sync_local_dir().latest_block()
#                 index = int(prev_block.index) + 1
#                 prev_hash = prev_block.hash
#                 break
#
#             else:
#                 # Assign genesis block attributes
#                 index = 0
#                 prev_hash = ''
#
#     # Assign block attributes according to supplied previous block
#     else:
#         index = int(prev_block.index) + 1
#         prev_hash = prev_block.hash
#
#     if not data:
#         merkleRoot, data = load_txns()
#
#     else:
#         hashList = []
#         for txn in data:
#             hashList.append(txn['id'])
#
#         merkleRoot = merkle(hashList)
#
#     if not origin:
#         filename = '%s/data.txt' % (CHAINDATA_DIR)
#         with open(filename, 'r') as origin_file:
#             origin = origin_file.read()
#
#     if not timestamp:
#         timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
#
#     nonce = 0
#     block_info_dict = dict_from_block_attributes(index=index, timestamp=timestamp, prev_hash=prev_hash, hash=None,
#                                                  origin=origin, merkle=merkleRoot, nonce=nonce, data=data)
#
#     new_block = block.Block(block_info_dict)
#
#     return new_block
#
#
# Function to load transaction from the local directory and return the Merkle root
def load_txns():
    # Initialise a transaction database object from the local directory
    txn_db = txn.trans_db()
    txn_db.sync_local_dir()

    # Add the first n transaction to the new block
    data = txn_db.trans[0:NUM_TXNS]

    if len(data) == 0:
        # Return the Merkel root of a blank string without computation
        merkleRoot = '0000000000000000000000000000000000000000000000000000000000000000'

    else:
        hashList = []
        for transaction in data:
            hashList.append(transaction['id'])

        merkleRoot = merkle(hashList)

    return merkleRoot, data


# Function to compute the combines value of two hashes
def hash2(hash_a, hash_b):
    # Reverse inputs before and after hashing due to big-endian / little-endian nonsense
    combinedHash = hash_a[::-1] + hash_b[::-1]

    # Compute hash of the combined hash values
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


def node_txt(port):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    addr = str(ip_address) + ':' + str(port)

    filename = '%s/data.txt' % (CHAINDATA_DIR)
    with open(filename, 'w') as data_file:
        data_file.write(addr)


# # THIS IS ONLY USED AS A TESTING FUNCTION
# def find_valid_nonce(find_block, data=None):
#     find_block.nonce = 0
#     find_block.update_self_hash()  # calculate_hash(index, prev_hash, data, timestamp, nonce)
#     if not find_block.data:
#         find_block.data = data
#     while str(find_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
#         find_block.nonce += 1
#         find_block.update_self_hash()
#     assert find_block.is_valid()
#     return find_block


def update_status(port):
    # Gather LAN IP address of the host computer
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    time_stamp = datetime.utcnow().strftime('%Y%m%d%H%M')

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    # Send a post request to the node server
    try:
        requests.post(server_addr + '/new_node', json=(str(ip_address) + ':' + str(port), time_stamp))

    except requests.exceptions.RequestException as error:
        print(error)

    # Send a post request to the active nodes
    for addr in db.active_nodes:
        try:
            requests.post('http://' + addr + '/new_node', json=(str(ip_address) + ':' + str(port), time_stamp))

        except requests.exceptions.RequestException as error:
            print(error)


def send_txn(txn):
    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    txn = {key: val for key, val in ([('id', None)] + list(txn.items()) + [('trans_type', 'Origination')])}
    txn_str = str(txn['lender']) + str(txn['borrower']) + str(txn['type']) + str(txn['security']) + str(txn['price']) + str(txn['variance']) + str(txn['quantity']) + str(txn['expiration'])
    sha = hashlib.sha256()
    sha.update(txn_str.encode('utf-8'))
    txn['id'] = sha.hexdigest()

    # Send the transaction as a POST request to all nodes
    for addr in db.active_nodes:
        try:
            requests.post('http://' + addr + '/transaction', json=txn)

        except requests.exceptions.RequestException as error:
            print(error)


def sanitise_local_dir(port):
    if os.path.exists(CHAINDATA_DIR):
        shutil.rmtree(CHAINDATA_DIR)

    os.mkdir(CHAINDATA_DIR)

    # Save .txt file with info about what port a given node in running on
    node_txt(port)


# if __name__ == '__main__':
    # block = create_new_block()
    # print(block)
    #
    # block.update_merkle()
    #
    # print(block)
