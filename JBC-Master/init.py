import requests
from tqdm import tqdm
import os
import json
import glob

# Import from custom scripts
import sync
import genesis
import utils
from config import *


def init():
    print('Scanning network for peer nodes:')
    available_ports = []
    occupied_ports = []
    for port in tqdm(range(5000, 5003)):  # SOMEHOW MAKE THIS INCLUSIVE SO YOU KNOW WHAT PORTS
        # Check through the list of defined ports to see if any nodes are running
        peer_blockchain_url = 'http://localhost:' + str(port)
        try:
            r = requests.get(peer_blockchain_url)

        except requests.exceptions.ConnectionError:
            available_ports.append(port)

        else:
            occupied_ports.append(port)

    print('Node(s) running at: %s' % occupied_ports)
    print('Available ports at: %s' % available_ports)

    # port = input('Enter port to start node: ')
    # REFINE LOGIC TO SANITISE USER ENTRY
    # while port not in ports:
    #     port = input('ERROR: port not available, enter valid port: ')

    port = 5002
    print('Node started on port: %s' % port)

    # Save .txt file with info about what port a given node in running on
    utils.node_txt(port)

    # Condition for no running nodes on network
    if len(occupied_ports) == 0:
        print('No nodes running on network')
        # Check if there are JSON files in local directory
        if os.path.exists(CHAINDATA_DIR):
            # Ask user if they want to reload previous data
            while True:
                answer = input('Previous blockchain data detected, attempt to reload (Y/N)?: ')
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
        print('Connecting to peer nodes...')
        # Sync with nodes across network and download the latest blockchain data to local directory
        sync.sync(save=False)
        print('Sync complete, local directory updated')

    return port
