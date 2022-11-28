import os
import utils
import glob
import shutil

# Import from custom scripts
from config import *


def genesis(port):
    # Sanitise local directory
    if os.path.exists(CHAINDATA_DIR):
        shutil.rmtree(CHAINDATA_DIR)

    os.mkdir(CHAINDATA_DIR)

    # Save .txt file with info about what port a given node in running on
    utils.node_txt(port)

    # Create first block object and save to local directory
    first_block = mine_first_block(port)
    first_block.self_save()
    print(first_block.__dict__)


def mine_first_block(port):
    # Create block object and mine to find valid hash that meets the required difficulty
    first_block = utils.create_new_block_from_prev(prev_block=None, data=None)  # CLARIFY THIS IN THE FUTURE
    first_block.update_self_hash()
    while str(first_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
        first_block.nonce += 1
        first_block.update_self_hash()

    assert first_block.is_valid()
    return first_block

genesis(5000)
