import aiohttp
import asyncio
import time
import os
import json
import glob

# Import from custom scripts
from chain import Chain
from config import *
from block import Block
import database
import transaction as txn


# Function to create chain object from local directory
def sync_local_dir():
    blocks = []
    # Assumes that the local directory has data stored
    if os.path.exists(CHAINDATA_DIR):
        for filepath in glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
            with open(filepath, 'r') as block_file:
                try:
                    # Read local JSON block data stored in directory
                    block_info = json.load(block_file)
                    block_file.close()

                except IOError as e:
                    print(f'Cannot open {filepath}')

                # Create block object from local JSON data
                local_block = Block(block_info)
                # Append block objects into a list
                blocks.append(local_block)

    # Ensure block objects are ordered according to index
    blocks.sort(key=lambda block: block.index)
    # Create chain object from list of block objects
    local_chain = Chain(blocks)

    return local_chain


async def get_blockchain(session, addr):
    try:
        async with session.get(addr) as response:
            if response.status == 200:
                # Store the given peer node's JSON object as a chain object
                peer_blockchain_dict = await response.json(content_type=None)

                # Convert the JSON objects to a list of block objects
                peer_blocks = [Block(bdict) for bdict in peer_blockchain_dict]
                # Convert the list of block objects to a chain object to check its validity
                peer_chain = Chain(peer_blocks)

                return peer_chain

            else:
                print(response.status)

    except aiohttp.ClientConnectorError as e:
        print(f'Peer at {addr.split("/")[2]} not running')


async def sync_overall(save=False):
    best_chain = sync_local_dir()  # THIS NEEDS TO BE CHANGED ACCORDING TO CONSENSUS ALGORITHM

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    async with aiohttp.ClientSession() as session:
        tasks = []
        start_time = time.time()
        for addr in db.active_nodes:
            url = f'http://{addr}/blockchain'
            tasks.append(asyncio.ensure_future(get_blockchain(session, url)))

        data = await asyncio.gather(*tasks)
        for peer_chain in data:
            # Exception handling for when no data is returned from a node address
            if peer_chain is None:
                continue

            # THIS IS THE CONSENSUS ALGORITHM - NEEDS WORK
            if peer_chain.is_valid() and len(peer_chain) > len(best_chain):
                best_chain = peer_chain

    print("Longest blockchain is %s blocks" % len(best_chain))

    # Save and replace local directory according to 'save' argument
    if save:
        # Remove all JSON files in the local directory - NEEDS REFINEMENT
        for filepath in glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
            os.remove(filepath)

        # Save the new chain in the local directory
        best_chain.self_save()
        print(best_chain.txn_list())

    print("--- Blockchain sync time: %s seconds ---" % (time.time() - start_time))

    return best_chain


def validity_sync():
    local_chain = sync_local_dir()
    if not local_chain.is_valid():
        print('LOCAL CHAIN IS CORRUPT, SYNCING WITH NETWORK')
        sync(save=True)

    return


def sync(save=False):
    chain = asyncio.run(sync_overall(save=save))
    asyncio.run(sync_transactions())

    return chain


async def get_trans(session, addr):
    try:
        async with session.get(addr) as response:
            if response.status == 200:
                # Return a given node's transactions
                return await response.json(content_type=None)

            else:
                print(response.status)

    except aiohttp.ClientConnectorError as e:
        print(f'Peer at {addr.split("/")[2]} not running')


async def sync_transactions():
    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    # Initialise a transaction database object from the local directory
    txn_db = txn.trans_db()
    txn_db.sync_local_dir()

    async with aiohttp.ClientSession() as session:
        tasks = []
        start_time = time.time()
        for addr in db.active_nodes:
            url = f'http://{addr}/get_transactions'
            tasks.append(asyncio.ensure_future(get_trans(session, url)))

        data = await asyncio.gather(*tasks)

        pending_trans = []
        for txns_list in data:
            for transaction in txns_list:
                if (not transaction in pending_trans) and (not transaction in txn_db.trans):
                    pending_trans.append(transaction)

    # Initialise a transaction database object from the local directory
    txn_db = txn.trans_db()
    txn_db.sync_local_dir()

    # Add new node address to the database and save to the local directory
    txn_db.trans = txn_db.trans + pending_trans
    txn_db.self_save()

    print("--- Transaction sync time: %s seconds ---" % (time.time() - start_time))

    return


if __name__ == '__main__':
    sync(save=True)
