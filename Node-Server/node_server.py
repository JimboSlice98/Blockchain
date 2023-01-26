from flask import Flask, jsonify, request
import json
from apscheduler.schedulers.background import BackgroundScheduler
import database

node = Flask(__name__)
sched = BackgroundScheduler(standalone=True)


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

    # Add new node address to the database and save to the local directory
    if ip_addr == data[0].split(':')[0]:
        db.active_nodes[data[0]] = data[1]
        db.self_save()

    # Exception handling if a node tries to send incorrect node information
    else:
        print('ERROR: IP addresses do not match')
        print('Request IP address: %s\nData IP address:    %s' % (ip_addr, data[0].split(':')[0]))

    return jsonify(received=True)


if __name__ == '__main__':
    # Initialise the database for storing addresses of active nodes on the network and update local directory
    db = database.node_db()
    db.self_save()

    # Add a database cleaning job and start the BackgroundScheduler
    sched.add_job(db.clean, 'interval', minutes=5)
    sched.start()

    # Start the FLASK server
    node.run(host='0.0.0.0', port=5050)
