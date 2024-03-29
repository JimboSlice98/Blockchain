import requests
from tqdm import tqdm
import logging
import os
import sys
import glob
import socket

# Import from custom scripts
import sync
import database
import genesis
import utils
import config
from config import *


# Supress logging being printed to the terminal
logging.getLogger('urllib3').propagate = False


def init():
    # Create database object to store addresses from the node server
    db = database.node_db()
    server_addr = config.server_addr

    print('Connecting to server to get node addresses...')
    # Exception handling for not reaching the server
    con_err = 1
    while con_err == 1:
        # Try to connect to the predefined server address
        try:
            r = requests.get(server_addr + '/get_nodes').json()
            db.active_nodes = r['active_nodes']
            db.inactive_nodes = r['inactive_nodes']
            con_err = 0

        # Connection unsuccessful so ask user for new address
        except requests.exceptions.RequestException:
            print('ERROR: Server not reachable')
            server_addr = input('Enter server address: ')
            print('Connecting to server...')
            con_err = 1

    db.self_save()
    print('Data downloaded')
    print('Finding available ports...')

    target = socket.gethostbyname(socket.gethostname())
    available_ports = []
    occupied_ports = []

    try:
        # Scan all ports from 5000->5050
        for port in tqdm(range(5000, 5004)):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # Append occupied port to list
            if s.connect_ex((target, port)) == 0:
                occupied_ports.append(port)

            else:
                available_ports.append(port)

            s.close()

    except socket.gaierror:
        print('\n ERROR: Hostname could not be resolved')
        sys.exit()

    except socket.error:
        print('\n ERROR: Server not responding')
        sys.exit()

    print('Occupied port(s): %s' % occupied_ports)

    # Allow user to select port to run the node
    port = int(input('Enter port [5000-5003] to start node: '))
    while True:
        if port in available_ports:
            break

        else:
            port = int(input('ERROR: port not available, enter valid port: '))

    # Send post request to server and active nodes on the network
    utils.update_status(port)

    print('Node started on port: %s' % port)

    ip_address = socket.gethostbyname(socket.gethostname())

    # Delete the node's own address from the database
    if (ip_address + ':' + str(port)) in db.active_nodes:
        del db.active_nodes[ip_address + ':' + str(port)]

    # ------------------------------------
    # BIG LOGIC FOR STARTING NODE
    # ------------------------------------

    # Condition for no running nodes on network
    if len(db.active_nodes) == 0:
        print('No nodes running on network')
        # Check if there are JSON files in local directory
        if glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
            # Ask user if they want to reload previous data
            while True:
                answer = input('Previous blockchain data detected, attempt to reload? (Y/N): ')
                if answer.upper() == 'Y':
                    print('Loading previous blockchain data...')
                    local_chain = sync.sync_local_dir()
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
        print('%d nodes running on network' % len(db.active_nodes))
        utils.sanitise_local_dir(port)
        print('Downloading latest blockchain data...')
        sync.sync(save=True)
        print('Download complete')

        # # Check if there are JSON files in local directory
        # if glob.glob(os.path.join(CHAINDATA_DIR, '*.json')):
        #     # CONSENSUS ALGORITHM NEEDED
        #     print('Warning: Consensus algorithm needed here, not yet implemented')
        #     print('Creating genesis block...')
        #     # Create the first block from scratch
        #     genesis.genesis(port)
        #     print('Genesis block created')
        #
        # # No JSON files in local directory
        # else:
        #     print('Downloading latest blockchain data...')
        #     sync.sync(save=True)
        #     print('Download complete')
        #
        #     # Save .txt file with info about what port a given node in running on
        #     utils.node_txt(port)
        #
        #     # print('Creating genesis block...')
        #     # # Create the first block from scratch
        #     # genesis.genesis(port)
        #     # print('Genesis block created')

    return port
