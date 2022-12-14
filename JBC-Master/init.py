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

    # Use websockets to check if any nodes are running on the network
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    for port in range(5000, 5003):  # SOMEHOW MAKE THIS INCLUSIVE SO YOU KNOW WHAT PORTS
        # Scan through listed in config.py
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
    # BIG LOGIC FOR STARTING NODE
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
            print('Downloading latest blockchain data...')
            sync.sync(save=True)
            print('Download complete')

            # Save .txt file with info about what port a given node in running on
            utils.node_txt(port)

            # print('Creating genesis block...')
            # # Create the first block from scratch
            # genesis.genesis(port)
            # print('Genesis block created')

    return port
