import json
from flask import Flask, jsonify, request
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler

# Import from custom scripts
from block import Block
import sync
import mine
import init
import database
import utils

# Create Flask server, BackgroundScheduler and Database object
node = Flask(__name__)
sched = BackgroundScheduler(standalone=True)
mine.sched = sched
db = database.node_db()


# Function to return the blockchain stored on a given node when queried
@node.route('/blockchain.json', methods=['GET'])
def blockchain():
    # Ensure the chain object on a given node is synced with local directory
    local_chain = sync.sync_local_dir()

    # Convert blocks to dictionaries then send as JSON objects
    json_blocks = json.dumps(local_chain.block_list_dict())

    print(local_chain.block_list_dict())
    print(json_blocks)

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


if __name__ == '__main__':
    # Initialisation sequence of node
    port = init.init()

    # Add a mining job to the BackgroundScheduler
    # sched.add_job(mine.mine_for_block, kwargs={'rounds': STANDARD_ROUNDS, 'start_nonce': 0}, id='mining')
    # Add a listener to detect when mine job has been executed
    sched.add_listener(mine.mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)

    # Add the database cleaning and status update job to the BackgroundScheduler
    sched.add_job(db.clean, 'interval', minutes=5)
    sched.add_job(utils.update_status, 'interval', kwargs={'port': port}, minutes=1)

    # Start the BackgroundScheduler
    sched.start()

    # Start the FLASK server
    node.run(host='0.0.0.0', port=port)
