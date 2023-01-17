from flask import Flask, jsonify, request
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


node = Flask(__name__)
sched = BackgroundScheduler(standalone=True)


class node_db(object):
    def __init__(self):
        self.master_nodes = {}
        self.active_nodes = {}
        self.inactive_nodes = {}

    def db_to_dict(self):
        data = {"master_nodes": self.master_nodes,
                "active_nodes": self.active_nodes,
                "inactive_nodes": self.inactive_nodes}

        return data

    # Method to save database to local directory
    def self_save(self):
        # Nest dictionaries to create a single object
        data = self.db_to_dict()

        # Save data object as JSON file
        filename = 'node_database.json'
        with open(filename, 'w') as database:
            json.dump(data, database)

    # Method to populate the  database object from the local directory
    def sync_local_dir(self):
        filepath = 'node_database.json'
        if os.path.exists(filepath):
            with open(filepath, 'r') as data_file:
                try:
                    # Read JSON database file stored in local directory
                    data = json.load(data_file)

                except:
                    print(filepath)

        self.master_nodes = data['master_nodes']
        self.active_nodes = data['active_nodes']
        self.inactive_nodes = data['inactive_nodes']

    def clean(self):
        self.sync_local_dir()
        time_stamp = int(datetime.utcnow().strftime('%Y%m%d%H%M'))

        move_addr = []
        del_addr = []

        # Iterate through the active node addresses and remove inactive nodes (>10 mins)
        for key in self.active_nodes:
            if time_stamp - int(self.active_nodes[key]) > 10:
                # Add inactive node to the inactive list
                self.inactive_nodes[key] = self.active_nodes[key]
                move_addr.append(key)

        # Iterate through the inactive node addresses and remove dead nodes (>1 day)
        for key in self.inactive_nodes:
            # Add inactive node to the inactive list
            if time_stamp - int(self.inactive_nodes[key]) > 2400:
                del_addr.append(key)

        # Delete inactive nodes from the active list
        for key in move_addr:
            del self.active_nodes[key]

        # Delete dead nodes from the inactive list
        for key in del_addr:
            del self.inactive_nodes[key]

        self.self_save()


# Function to return a dictionary containing the addresses of active nodes on the network
@node.route('/get_nodes', methods=['GET'])
def get_nodes():
    # Initialise a database object from the local directory
    db = node_db()
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
    db = node_db()
    db.sync_local_dir()

    # Exception handling if a node tries to send incorrect node information
    if ip_addr == data[0]:
        print('HTML request IP address does not match received data')

    # Add new node address to the database and save to the local directory
    db.active_nodes[data[0]] = data[1]
    db.self_save()

    return jsonify(received=True)


if __name__ == '__main__':
    # Logic to initialise database depending on the local directory
    # ENTER LOGIC HERE!

    # # Initialise the database for storing addresses of active nodes on the network and update local directory
    node_database = node_db()
    node_database.self_save()

    # Add a database cleaning job and start the BackgroundScheduler
    sched.add_job(node_database.clean, 'interval', seconds=1)
    sched.start()

    # Start the FLASK server
    node.run(host='0.0.0.0', port=5050)
