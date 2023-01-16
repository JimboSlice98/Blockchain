from flask import Flask, jsonify, request
import os
import json


node = Flask(__name__)


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


# Function to create a database object from the local directory
def sync_local_db():
    node_database = node_db()
    filepath = 'node_database.json'
    if os.path.exists(filepath):
        with open(filepath, 'r') as data_file:
            try:
                # Read JSON database file stored in local directory
                data = json.load(data_file)

            except:
                print(filepath)

    node_database.master_nodes = data['master_nodes']
    node_database.active_nodes = data['active_nodes']
    node_database.inactive_nodes = data['inactive_nodes']

    return node_database


# Function to return a dictionary containing the addresses of active nodes on the network
@node.route('/get_nodes', methods=['GET'])
def get_nodes():
    # Initialise a database object reading information stored in the local directory
    db = sync_local_db()

    # Convert database to JSON object to be sent over HTML
    json_data = json.dumps(db.db_to_dict())

    return json_data


# Function to receive the address of a new node and append to the database
@node.route('/new_node', methods=['POST'])
def new_node():
    ip_addr = str(request.remote_addr)

    print(ip_addr)

    data = str(request.get_json())

    print(data)

    return jsonify(received=True)


if __name__ == '__main__':

    # node_database = sync_local_db()

    # Logic to initialise database depending on the local directory
    # ENTER LOGIC HERE!

    # # Initialise the database for storing addresses of active nodes on the network
    # node_database = node_db()
    # node_database.active_nodes = {"146.169.252.144:5000": "2023-01-16--17:19:17",
    #                               "146.169.170.245:5000": "2023-01-16--17:20:21"}
    # node_database.inactive_nodes = {"192.168.0.1:5000": "2023-01-09--22:41:30"}
    # node_database.self_save()

    # print(node_database.master_nodes, node_database.active_nodes, node_database.inactive_nodes)

    # Start the FLASK server
    node.run(host='0.0.0.0', port=5050)
