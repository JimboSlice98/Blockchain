from datetime import datetime
import block
import socket
import requests
import database
import os
import utils
import shutil

# Import from custom scripts
from config import *


def dict_from_block_attributes(**kwargs):
    info = {}
    for key in kwargs:
        if key in BLOCK_VAR_CONVERSIONS:
            info[key] = BLOCK_VAR_CONVERSIONS[key](kwargs[key])

        else:
            info[key] = kwargs[key]

    return info


def create_new_block(prev_block=None, data=None, timestamp=None):
    if not prev_block:
        # index zero and arbitrary previous hash
        index = 0
        prev_hash = ''
    else:
        index = int(prev_block.index) + 1
        prev_hash = prev_block.hash

    if not data:
        filename = '%s/data.txt' % (CHAINDATA_DIR)
        with open(filename, 'r') as data_file:
            data = data_file.read()

    if not timestamp:
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

    nonce = 0
    block_info_dict = dict_from_block_attributes(index=index, timestamp=timestamp, prev_hash=prev_hash, hash=None, data=data, nonce=nonce)
    new_block = block.Block(block_info_dict)
    return new_block


def node_txt(port):
    filename = '%s/data.txt' % (CHAINDATA_DIR)
    with open(filename, 'w') as data_file:
        data_file.write('Block mined by node on port %s' % port)


# THIS IS ONLY USED AS A TESTING FUNCTION
def find_valid_nonce(find_block, data=None):
    find_block.nonce = 0
    find_block.update_self_hash()  # calculate_hash(index, prev_hash, data, timestamp, nonce)
    if not find_block.data:
        find_block.data = data
    while str(find_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
        find_block.nonce += 1
        find_block.update_self_hash()
    assert find_block.is_valid()
    return find_block


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
    utils.node_txt(port)
