import pyfiglet
from datetime import datetime
import json
from flask import Flask, jsonify, request
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Import from custom scripts
import init
import database


# Create Flask server, BackgroundScheduler and Database object
node = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# db = database.node_db()


# Function to return the blockchain stored on a given node when queried
@node.route('/transaction', methods=['GET'])
def blockchain():
    return


# Function to receive a given block as a dictionary from another node
@node.route('/mined', methods=['POST'])
def mined():
    return


# Function to return a dictionary containing the addresses of active nodes on the network
@node.route('/get_nodes', methods=['GET'])
def get_nodes():
    return


# Function to receive the address of a new node and append to the database
@node.route('/new_node', methods=['POST'])
def new_node():
    return


if __name__ == '__main__':
    # Add Banner
    print('-' * 50)
    print('Blockchain Client Interface v1.9.20')
    print('-' * 50)

    # port = init.init()

    # ascii_banner = pyfiglet.figlet_format('WELCOME')
    # print(ascii_banner)

    # Start the FLASK server
    node.run(host='0.0.0.0', port=5020)
