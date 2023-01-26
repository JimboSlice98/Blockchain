import requests
import apscheduler

# Import from custom scripts
from block import Block
from config import *
import utils
import sync
import database


sched = None


# Function 1
def mine_for_block(chain=None, rounds=STANDARD_ROUNDS, start_nonce=0, timestamp=None):
    # If no chain object is passed as an argument, gather last block from local directory
    if not chain:
        chain = sync.sync_local_dir()

    # Gather last block from chain object argument
    prev_block = chain.most_recent_block()
    return mine_from_prev_block(prev_block, rounds=rounds, start_nonce=start_nonce, timestamp=timestamp)


# Function 2
def mine_from_prev_block(prev_block, rounds=STANDARD_ROUNDS, start_nonce=0, timestamp=None):
    # create new block with correct
    new_block = utils.create_new_block(prev_block=prev_block, timestamp=timestamp)
    return mine_block(new_block, rounds=rounds, start_nonce=start_nonce)


# Function 3
def mine_block(new_block, rounds=STANDARD_ROUNDS, start_nonce=0):
    # Mine a given block with nonce values in the range dictated by 'start_nonce' and 'rounds'
    # print('MINING FOR BLOCK %s. START NONCE: %s, ROUNDS: %s' % (new_block.index, start_nonce, rounds))
    nonce_range = [i+start_nonce for i in range(rounds)]
    for nonce in nonce_range:
        new_block.nonce = nonce
        new_block.update_self_hash()
        # If a valid nonce value has been found, the block has been mined
        if str(new_block.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
            print('BLOCK %s MINED. NONCE: %s' % (new_block.index, new_block.nonce))
            assert new_block.is_valid()
            return new_block, rounds, start_nonce, new_block.timestamp

    # The block could not be mined with the available nonce values, return the 'start_nonce' and 'rounds' for next job
    return None, rounds, start_nonce, new_block.timestamp


# Function triggered upon execution of mining job from BackgroundScheduler
def mine_for_block_listener(event):
    # Ensure the function is only called for upon mining job completion only
    if event.job_id == 'mining':
        # Receives a tuple from the scheduler upon job execution
        new_block, rounds, start_nonce, timestamp = event.retval
        # If the new block has been mined
        if new_block:
            # Save new block and broadcast to peer nodes
            print('SAVING BLOCK...')
            new_block.self_save()
            print('BLOCK SAVED')
            print('BROADCASTING BLOCK TO NETWORK...')
            broadcast_mined_block(new_block)
            print('BROADCAST COMPLETE')

            # Restart the mining job for the next block
            sched.add_job(mine_from_prev_block, args=[new_block], kwargs={'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining')

        # No new block has been mined so restart the mining job with increased 'start_nonce'
        else:
            # print('\n\nROUNDS FINISHED, THEREFORE RESTARTING MINING')
            sched.add_job(mine_for_block, kwargs={'rounds': rounds, 'start_nonce': start_nonce+rounds, 'timestamp': timestamp}, id='mining')


# Function to broadcast a given mined block to the network
def broadcast_mined_block(new_block):
    block_info_dict = new_block.to_dict()

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    # Broadcast JSON object via post request to active nodes only
    for addr in db.active_nodes:
        try:
            requests.post('http://' + addr + '/mined', json=block_info_dict)

        except requests.exceptions.RequestException as error:
            print(error)
            print('Peer at %s not running. Continuing to next peer.' % addr)

    return True


# Function to determine if the received block is valid
def validate_possible_block(possible_block):
    # Gather the most current local block to validate possible new block
    chain = sync.sync_local_dir()
    cur_block = chain.most_recent_block()

    # Check point 1) Are the indexes in order
    if possible_block.index - 1 != cur_block.index:
        print('VPB: Index error')
        return False

    # Check point 2) Are the has values linked
    if possible_block.prev_hash != cur_block.hash:
        print('VPB: Hash error')
        return False

    # Check point 3) Is the hash of a block correct and does it meet the difficulty
    if not possible_block.is_valid():
        print('VPB: Block invalid')
        return False

    # Therefore the new block is valid so needs to be saved
    possible_block.self_save()
    # Remove all mining jobs as they will contain higher nonce ranges
    try:
        sched.remove_job('mining')
        print("removed running mine job in validating possible block")
    except apscheduler.jobstores.base.JobLookupError:
        print("mining job didn't exist when validating possible block")

    # Restart the mining for the next block after the received block
    sched.add_job(mine_for_block, kwargs={'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining')

    return True
