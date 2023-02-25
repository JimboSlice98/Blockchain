import aiohttp
import asyncio
import requests
import os
from datetime import datetime

from block import Block
import utils
import database
import sync
from config import *


async def broadcast_block(new_block):
    block_info_dict = new_block.to_dict()

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    accepted = []
    rejected = []
    dead = []

    aiohttp.ClientTimeout(total=2, connect=2, sock_connect=2, sock_read=2)
    async with aiohttp.ClientSession() as session:
        for addr in db.active_nodes:
            url = f'http://{addr}/mined'
            print(url)
            try:
                async with session.post(url, json=block_info_dict) as response:
                    # if response.status == 200:
                    # status = await response.json()

                    print(response.status)

            except aiohttp.ClientConnectorError as e:
                print(f'Peer at {addr} not running')


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
        data = []

    if not origin:
        filename = '%s/data.txt' % (CHAINDATA_DIR)
        with open(filename, 'r') as origin_file:
            origin = origin_file.read()

    if not timestamp:
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

    nonce = 0
    block_info_dict = dict_from_block_attributes(index=750, timestamp=timestamp, prev_hash=prev_hash,
                                                 hash=None, origin=origin, nonce=nonce, data=data)
    new_block = block.Block(block_info_dict)

    return new_block


# Function to broadcast a given mined block to the network
def broadcast_mined_block(new_block):
    block_info_dict = new_block.to_dict()

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    accepted = []
    rejected = []
    dead = []

    # Broadcast JSON object via post request to active nodes only
    for addr in db.active_nodes:
        try:
            r = requests.post('http://' + addr + '/mined', json=block_info_dict)

        except requests.exceptions.RequestException as error:
            print(error)
            print('Peer at %s not running. Continuing to next peer.' % addr)
            dead.append(addr)

            continue

        # Handling for when a node accepts the block
        if r.status_code == 200:
            accepted.append(addr)

        # Handling for when a node refuses the broadcast block
        if r.status_code == 409:
            print('Peer at %s refused block: %s' % (addr, new_block.index))
            rejected.append(addr)

    # # Remove dead nodes from database
    # for addr in dead:
    #     db.remove(addr)

    print('A:', len(accepted), ' R:', len(rejected), ' D:', len(dead))

    # Only save the block if it is accepted by the network
    if len(accepted) + len(rejected) == 0:
        new_block.self_save()
        return True

    if len(accepted) / (len(accepted) + len(rejected)) >= 0.51:
        new_block.self_save()
        return True

    else:
        print('Rejected')
        return False


if __name__ == '__main__':
    block = Block({"index": "1400", "timestamp": "20230221194603884220", "prev_hash": "000000dff19a9561b97f74cac54578812fc6e4208b36d929ab47071d04b2ffcb", "hash": "0000004f8fe946b666688c01df7cb5f5641c7ee119177a383b43f58f012d0300", "origin": "155.198.40.159:5000", "nonce": "421646", "data": "[]"})

    print(block.index,
          block.timestamp,
          block.prev_hash,
          block.hash,
          block.origin,
          block.nonce,
          block.data)

    broadcast_mined_block(block)

    # text = asyncio.run(broadcast_block(block))
