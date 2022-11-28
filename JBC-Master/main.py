import datetime
import json
import hashlib
import requests
from tqdm import tqdm
import os
import glob
import apscheduler
from flask import Flask, jsonify, request
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import sys
import argparse
import logging

# Import from custom scripts
from block import Block
from config import *
import utils
import sync
import genesis
import mine
import init


node = Flask(__name__)
sched = BackgroundScheduler(standalone=True)


# Function to return the blockchain stored on a given node when queried
@node.route('/blockchain.json', methods=['GET'])
def blockchain():
    # Ensure the chain object on a given node is synced with local directory
    local_chain = sync.sync_local()

    # Convert blocks to dictionaries then send as JSON objects
    json_blocks = json.dumps(local_chain.block_list_dict())

    return json_blocks


# Function to receive a given block as a dictionary from another node
@node.route('/mined', methods=['POST'])
def mined():

    possible_block_dict = request.get_json()
    possible_block = Block(possible_block_dict)
    print(possible_block_dict)
    print(sched.get_jobs())
    print(sched)

    sched.add_job(mine.validate_possible_block, args=[possible_block_dict], id='validate_possible_block') #add the block again

    return jsonify(received=True)


if __name__ == '__main__':

    print('Debugging is soo much fun...')

    # Initialisation sequence of node
    port = init.init()

    # Start the FLASK server
    # Create BackgroundScheduling object
    mine.sched = sched  # to override the BlockingScheduler in the
    # only mine if we want to
    if True:
        # in this case, sched is the background sched
        sched.add_job(mine.mine_for_block, kwargs={'rounds': STANDARD_ROUNDS, 'start_nonce': 0},
                      id='mining')  # add the block again
        sched.add_listener(mine.mine_wfor_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)  # args=sched)

    sched.start()  # want this to start, so we can validate on the schedule and not rely on Flask

    # now we know what port to use
    node.run(host='127.0.0.1', port=port)
