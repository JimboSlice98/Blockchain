from datetime import datetime
import block
import socket
import requests
import database
import os
import shutil
import hashlib

# Import from custom scripts
from config import *
import sync
import transaction as txn


def dict_from_block_attributes(**kwargs):
    info = {}
    for key in kwargs:
        if key in BLOCK_VAR_CONVERSIONS:
            info[key] = BLOCK_VAR_CONVERSIONS[key](kwargs[key])

        else:
            info[key] = kwargs[key]

    return info


def create_new_block(prev_block=None, timestamp=None, origin=None, data=None):
    if not prev_block:
        # Check the local directory for JSON files
        for fname in os.listdir(CHAINDATA_DIR):
            if fname.endswith('.json'):
                # Gather last block from local directory
                prev_block = sync.sync_local_dir().latest_block()
                index = int(prev_block.index) + 1
                prev_hash = prev_block.hash
                break

            else:
                # Assign genesis block attributes
                index = 0
                prev_hash = ''

    # Assign block attributes according to supplied previous block
    else:
        index = int(prev_block.index) + 1
        prev_hash = prev_block.hash

    if not data:
        # Initialise a transaction database object from the local directory
        txn_db = txn.trans_db()
        txn_db.sync_local_dir()

        # Add the first 20 transaction to the new block
        data = txn_db.trans[0:NUM_TXNS]

    if not origin:
        filename = '%s/data.txt' % (CHAINDATA_DIR)
        with open(filename, 'r') as origin_file:
            origin = origin_file.read()

    if not timestamp:
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

    nonce = 0
    block_info_dict = dict_from_block_attributes(index=index, timestamp=timestamp, prev_hash=prev_hash,
                                                 hash=None, origin=origin, nonce=nonce, data=data)
    new_block = block.Block(block_info_dict)

    return new_block


def load_txns():
    # Initialise a transaction database object from the local directory
    txn_db = txn.trans_db()
    txn_db.sync_local_dir()

    # Add the first 20 transaction to the new block
    data = txn_db.trans[0:NUM_TXNS]
    merkleRoot = merkle(data)


# Function to compute the combines value of two hashes
def hash2(a, b):
    # Reverse inputs before and after hashing due to big-endian / little-endian nonsense
    a1 = a[::-1]
    b1 = b[::-1]
    combinedHash = a1 + b1

    sha = hashlib.sha256()
    sha.update(combinedHash.encode('utf-8'))
    hash = sha.hexdigest()

    return hash


# Function to hash a pair of items recursively to find the Merkle root
def merkle(hashList):
    if len(hashList) == 1:
        return hashList[0]

    newHashList = []
    # Process pairs. For odd length, the last is skipped
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


def sanitise_local_dir(port):
    if os.path.exists(CHAINDATA_DIR):
        shutil.rmtree(CHAINDATA_DIR)

    os.mkdir(CHAINDATA_DIR)

    # Save .txt file with info about what port a given node in running on
    node_txt(port)
