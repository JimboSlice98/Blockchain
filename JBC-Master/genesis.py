import os
import utils
import glob

# Import from custom scripts
from config import *


def genesis(port):
    # Check if a local directory exists
    if not os.path.exists(CHAINDATA_DIR):
        os.mkdir(CHAINDATA_DIR)

    for filepath in glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
        os.remove(filepath)

    os.remove(filepath) for filepath in

    # Save .txt file with info about what port a given node in running on
    utils.node_txt(port)

    # Create first block object and save to local directory
    first_block = mine_first_block(port)
    first_block.self_save()


def mine_first_block(port):
    # Create block object and mine to find valid hash that meets the required difficulty
    first_block = utils.create_new_block_from_prev(prev_block=None, data=None)  # CLARIFY THIS IN THE FUTURE
    first_block.update_self_hash()
    while str(first_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
        first_block.nonce += 1
        first_block.update_self_hash()

    assert first_block.is_valid()
    return first_block
