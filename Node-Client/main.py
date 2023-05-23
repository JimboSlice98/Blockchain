import json
from flask import Flask, jsonify, request
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Import from custom scripts
from block import Block
import sync
import mine
import init
import database
import transaction as txn
import utils
from config import *


# Create Flask server, BackgroundScheduler and Database object
node = Flask(__name__)
sched = BackgroundScheduler(standalone=True)
mine.sched = sched
init.sched = sched
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
db = database.node_db()
trans_db = txn.trans_db()


# Function to return the blockchain stored on a given node when queried
@node.route('/blockchain', methods=['GET'])
def blockchain():
    # Pause the mining job to free headroom for sync
    sched.pause()

    # Ensure the chain object on a given node is synced with local directory
    local_chain = sync.sync_local_dir()

    # Convert blocks to dictionaries then send as JSON objects
    json_blocks = json.dumps(local_chain.block_list_dict())

    # Resume mining job
    sched.resume()

    return json_blocks


# Function to receive a given block as a dictionary from another node
@node.route('/mined', methods=['POST'])
def mined():
    # Pause the mining job to free headroom for sync
    sched.pause()

    network_block = Block(request.get_json())

    if not mine.validate_network_block(network_block):
        # Resume mining job
        sched.resume()

        return jsonify(received=False), 409

    # Resume mining job
    sched.resume()

    return jsonify(received=True)


# Function to return a dictionary containing the addresses of active nodes on the network
@node.route('/get_nodes', methods=['GET'])
def get_nodes():
    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    # Convert database to JSON object to be sent over HTML
    json_data = json.dumps(db.db_to_dict())

    return json_data


# Function to receive the address of a new node and append to the database
@node.route('/new_node', methods=['POST'])
def new_node():
    # Capture IP address from the HTML request, JSON data
    ip_addr = request.remote_addr
    data = request.get_json()

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    # Exception handling if a node tries to send incorrect address data
    if ip_addr != data[0].split(':')[0]:
        print('ERROR: IP addresses do not match')
        print('Request IP address: %s\nData IP address:    %s' % (ip_addr, data[0].split(':')[0]))

        return jsonify(received=True)

    # Delete active node from the inactive list
    if data[0] in db.inactive_nodes:
        del db.inactive_nodes[data[0]]

    # Add new node address to the database and save to the local directory
    db.active_nodes[data[0]] = data[1]
    db.self_save()

    return jsonify(received=True)


@node.route('/transaction', methods=['POST'])
def transaction():
    # Capture JSON data
    data = request.get_json()

    # Initialise a transaction database object from the local directory
    txn_db = txn.trans_db()
    txn_db.sync_local_dir()

    # Add new node address to the database and save to the local directory
    txn_db.trans.append(data)
    txn_db.self_save()

    return jsonify(received=True)


@node.route('/get_transactions', methods=['GET'])
def get_transactions():
    # Pause the mining job to free headroom for sync
    sched.pause()

    # Initialise a transaction database object from the local directory
    txn_db = txn.trans_db()
    txn_db.sync_local_dir()

    # Convert database to JSON object to be sent over HTML
    json_data = json.dumps(txn_db.trans)

    # Resume mining job
    sched.resume()

    return json_data


if __name__ == '__main__':
    # Initialisation sequence of node
    port = init.init()

    # # Add a mining job and listener to the BackgroundScheduler
    # if not sched.get_job('mining'):
    #     sched.add_job(mine.mine, kwargs={'block': utils.create_new_block(), 'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining')

    # sched.add_listener(mine.mine_listener, apscheduler.events.EVENT_JOB_EXECUTED)

    # Add the database cleaning,status update and validity sync jobs to the BackgroundScheduler
    sched.add_job(db.clean, 'interval', minutes=5, misfire_grace_time=None)
    sched.add_job(utils.update_status, 'interval', kwargs={'port': port}, minutes=1, misfire_grace_time=None)
    # sched.add_job(sync.validity_sync, 'interval', seconds=30, misfire_grace_time=None)
    # sched.add_job(mine.mine_sched, 'interval', seconds=30, misfire_grace_time=None)

    # Start the BackgroundScheduler
    sched.start()

    # Start the FLASK server
    node.run(host='0.0.0.0', port=port)
