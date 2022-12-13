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
    print('Block received from peer node: ')
    possible_block_dict = request.get_json()
    possible_block = Block(possible_block_dict)
    print(possible_block_dict)

    sched.add_job(mine.validate_possible_block, args=[possible_block], id='validate_possible_block')

    return jsonify(received=True)


if __name__ == '__main__':

    # Initialisation sequence of node
    port = init.init()

    # Create BackgroundScheduler object to override BlockingScheduler object in mine.py
    mine.sched = sched

    # Add a mining job to the BackgroundScheduler
    sched.add_job(mine.mine_for_block, kwargs={'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining')
    # Add a listener to detect when mine job has been executed
    sched.add_listener(mine.mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)

    # Start the BackgroundScheduler
    sched.start()

    # Start the FLASK server
    node.run(host='127.0.0.1', port=port)
