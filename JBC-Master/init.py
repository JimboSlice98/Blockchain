import requests
from tqdm import tqdm
import logging
import os
import json
import glob
import socket

# Import from custom scripts
import sync
import genesis
import utils
from config import *


# Supress logging being printed to the terminal
logging.getLogger('urllib3').propagate = False


def init():
    print('Scanning network for peer nodes:')
    available_ports = []
    occupied_ports = []
    # for port in tqdm(range(5000, 5003)):  # SOMEHOW MAKE THIS INCLUSIVE SO YOU KNOW WHAT PORTS
    #     # Check through the list of defined ports to see if any nodes are running
    #     peer_blockchain_url = 'http://localhost:' + str(port)
    #     try:
    #         r = requests.get(peer_blockchain_url)
    #
    #     except requests.exceptions.ConnectionError:
    #         available_ports.append(port)
    #
    #     else:
    #         occupied_ports.append(port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    for port in range(5000, 5003):  # SOMEHOW MAKE THIS INCLUSIVE SO YOU KNOW WHAT PORTS
        # Check through the list of defined ports to see if any nodes are running
        try:
            sock.connect(('127.0.0.1', port))

        except:
            available_ports.append(port)

        else:
            sock.close()
            occupied_ports.append(port)

    print('Node(s) running at: %s' % occupied_ports)
    print('Available ports at: %s' % available_ports)

    # Allow user to select port to run the node
    port = int(input('Enter port to run node: '))
    while True:
        if port in available_ports:
            break

        else:
            port = int(input('ERROR: port not available, enter valid port: '))

    print('Node started on port: %s' % port)

    # ------------------------------------
    # BIG FUCK-OFF LOGIC FOR STARTING NODE
    # ------------------------------------

    # Condition for no running nodes on network
    if len(occupied_ports) == 0:
        print('No nodes running on network')
        # Check if there are JSON files in local directory
        if glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
            # Ask user if they want to reload previous data
            while True:
                answer = input('Previous blockchain data detected, attempt to reload? (Y/N): ')
                if answer.upper() == 'Y':
                    print('Loading previous blockchain data...')
                    local_chain = sync.sync_local()
                    if local_chain.is_valid():
                        print('Previous blockchain data loaded successfully')
                        break

                    else:
                        print('Unable to load previous blockchain data as the files are corrupted')
                        print('Creating genesis block...')
                        # Create the first block from scratch
                        genesis.genesis(port)
                        print('Genesis block created')
                        break

                elif answer.upper() == 'N':
                    print('Creating genesis block...')
                    # Create the first block from scratch
                    genesis.genesis(port)
                    print('Genesis block created')
                    break

                else:
                    continue

        # No JSON files in local directory
        else:
            print('Creating genesis block...')
            # Create the first block from scratch
            genesis.genesis(port)
            print('Genesis block created')

    # Condition for running nodes on network
    else:
        # Check if there are JSON files in local directory
        if glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
            # CONSENSUS ALGORITHM NEEDED
            print('Warning: Consensus algorithm needed here, not yet implemented')
            print('Creating genesis block...')
            # Create the first block from scratch
            genesis.genesis(port)
            print('Genesis block created')

        # No JSON files in local directory
        else:
            print('Creating genesis block...')
            # Create the first block from scratch
            genesis.genesis(port)
            print('Genesis block created')

    return port


def check(host, port, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except:
        return False
    else:
        sock.close()
        return True


# print(check('127.0.0.1', 5000, timeout=1))
# print(check('127.0.0.1', 5001, timeout=1))

init()
