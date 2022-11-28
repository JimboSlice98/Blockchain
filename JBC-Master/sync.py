import os
import json
import requests
import glob

# Import from custom scripts
from chain import Chain
from config import *
from block import Block


# Function to create chain object from local directory
def sync_local():
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
    best_chain = sync_local()  # THIS NEEDS TO BE CHANGED ACCORDING TO CONSENSUS ALGORITHM
    for peer in PEERS:
        # Scan through the list of defined ports
        peer_blockchain_url = peer + 'blockchain.json'
        try:
            # Test to see is a node is running on a given port
            r = requests.get(peer_blockchain_url)

        except requests.exceptions.ConnectionError:
            print("Peer at %s not running. Continuing to next peer." % peer)

        else:
            print("Peer at %s is running. Gathered their blockchain for analysis." % peer)
            # Store the given peer node's JSON object as a chain object
            peer_blockchain_dict = r.json()
            peer_blocks = [Block(bdict) for bdict in peer_blockchain_dict]
            peer_chain = Chain(peer_blocks)
            assert peer_chain.is_valid()

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


def sync(save=False):

    return sync_overall(save=save)
