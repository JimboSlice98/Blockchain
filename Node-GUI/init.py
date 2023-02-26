import requests
from tqdm import tqdm
import logging
import os
import sys
import glob
import socket

# Import from custom scripts
import database
import config


# Supress logging being printed to the terminal
logging.getLogger('urllib3').propagate = False


def init():
    # Create database object to store addresses from the node server
    db = database.node_db()
    server_addr = config.server_addr
    node_addr = socket.gethostbyname(socket.gethostname())

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

    # Scan for occupied ports on a given node
    available_ports = []
    occupied_ports = []

    try:
        # Scan all ports from 5000->5050
        for port in tqdm(range(5000, 5004)):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # Append occupied port to list
            if s.connect_ex((node_addr, port)) == 0:
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

    print('Node started on port: %s' % port)

    # Delete the node's own address from the database
    if (node_addr + ':' + str(port)) in db.active_nodes:
        del db.active_nodes[node_addr + ':' + str(port)]
        db.self_save()

    return port
