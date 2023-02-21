import os
import json
import requests
import glob

# Import from custom scripts
from chain import Chain
from config import *
from block import Block
import database


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

                except:
                    print(filepath)

                # Create block object from local JSON data
                local_block = Block(block_info)
                # Append block objects into a list
                blocks.append(local_block)

    # Ensure block objects are ordered according to index
    blocks.sort(key=lambda block: block.index)
    # Create chain object from list of block objects
    local_chain = Chain(blocks)

    return local_chain


# Function to sync local directory with other nodes - CONSENSUS ALGORITHM IS HERE
def sync_overall(save=False):
    best_chain = sync_local_dir()  # THIS NEEDS TO BE CHANGED ACCORDING TO CONSENSUS ALGORITHM

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    # Query only active nodes for blockchain data
    for addr in db.active_nodes:
        try:
            r = requests.get('http://' + addr + '/blockchain.json')

        except requests.exceptions.RequestException as error:
            print(error)
            print('Peer at %s not running. Continuing to next peer.' % addr)

        else:
            # print("Peer at %s is running, gathered blockchain data for analysis" % addr)
            # Store the given peer node's JSON object as a chain object
            peer_blockchain_dict = r.json()
            # Convert the JSON objects to a list of block objects
            peer_blocks = [Block(bdict) for bdict in peer_blockchain_dict]
            # Convert the list of block objects to a chain object to check its validity
            peer_chain = Chain(peer_blocks)

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

    return best_chain


def validity_sync():
    local_chain = sync_local_dir()
    if not local_chain.is_valid():
        print('LOCAL CHAIN IS CORRUPT, SYNCING WITH NETWORK')
        sync(save=True)

    return


def sync(save=False):

    return sync_overall(save=save)
