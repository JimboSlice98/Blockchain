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


if __name__ == '__main__':
    local_chain = sync_local_dir()
    print(local_chain.is_valid())
