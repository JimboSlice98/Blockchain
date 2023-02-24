import requests
from datetime import datetime
import apscheduler

# Import from custom scripts
from block import Block
from config import *
import utils
import sync
import database


sched = None


def mine(block, rounds=STANDARD_ROUNDS, start_nonce=0):
    mined = False
    # Mine a given block with nonce values in the range dictated by 'start_nonce' and 'rounds'
    # print('MINING FOR BLOCK %s. START NONCE: %s, ROUNDS: %s' % (block.index, start_nonce, rounds))
    nonce_range = [start_nonce+i for i in range(rounds)]
    for nonce in nonce_range:
        block.nonce = nonce
        block.update_self_hash()
        # If a valid nonce value has been found, the block has been mined
        if str(block.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
            print('BLOCK %s MINED. NONCE: %s' % (block.index, block.nonce))
            assert block.is_valid()
            mined = True

            return block, rounds, start_nonce, mined

    # The block could not be mined with the available nonce values, return the 'start_nonce' and 'rounds' for next job
    # print('BLOCK NOT MINED, INCREASING NONCE RANGE')
    return block, rounds, start_nonce, mined


# Function triggered upon execution of mining job from BackgroundScheduler
def mine_listener(event):
    if event.job_id == 'mining':
        # Receives a tuple from the scheduler upon job execution
        new_block, rounds, start_nonce, status = event.retval
        # Check if the block has been mined
        if status:
            # Broadcast new block and start the mining job for the next block if accepted
            if broadcast_mined_block(new_block):
                next_block = utils.create_new_block(prev_block=new_block)
                sched.add_job(mine, kwargs={'block': next_block, 'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining', misfire_grace_time=None)
                print('BROADCAST COMPLETE')

            # The block has not been accepted by the network and the local directory has been updated
            else:
                sched.add_job(mine, kwargs={'block': utils.create_new_block(), 'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining', misfire_grace_time=None)

        # The block has not been mined so restart with an increased nonce range
        else:
            sched.add_job(mine, kwargs={'block': new_block, 'rounds': rounds, 'start_nonce': start_nonce+rounds}, id='mining', misfire_grace_time=None)


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
        sync.sync(save=True)
        return False


# Function to determine if the received block is valid
def validate_network_block(network_block):
    # Gather the most current local block to validate possible new block
    chain = sync.sync_local_dir()
    cur_block = chain.latest_block()

    # Check point 1) Are the indexes in order
    if network_block.index - 1 != cur_block.index:
        # print('VPB: Index error')
        return False

    # Check point 2) Are the has values linked
    if network_block.prev_hash != cur_block.hash:
        # print('VPB: Hash error')
        return False

    # Check point 3) Is the hash of a block correct and does it meet the difficulty
    if not network_block.is_valid():
        # print('VPB: Block invalid')
        return False

    # Therefore the new block is valid so needs to be saved
    network_block.self_save()
    # Remove all mining jobs as they will contain higher nonce ranges
    try:
        sched.remove_job('mining')
        print("Removed mining job as block is depreciated")
    except apscheduler.jobstores.base.JobLookupError as error:
        print(error)

    # Start mining for the next block after the received block
    next_block = utils.create_new_block(prev_block=network_block)
    sched.add_job(mine, kwargs={'block': next_block, 'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining', misfire_grace_time=None)

    return True


def mine_sched():
    if not sched.get_job('mining'):
        sched.add_job(mine, kwargs={'block': utils.create_new_block(), 'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining', misfire_grace_time=None)
