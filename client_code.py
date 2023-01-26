import requests
import socket
import sys
from datetime import datetime
from tqdm import tqdm

# Import from custom scripts
import database


# Create database object to store addresses from the node server
db = database.node_db()

print('Gathering peer node data from server...')

server_addr = 'http://146.169.254.109:5050/get_nodes'
try:
    r = requests.get(server_addr).json()
    db.active_nodes = r['active_nodes']
    db.inactive_nodes = r['inactive_nodes']

except requests.exceptions.ConnectionError:
    print('ERROR: Server not reachable')

db.self_save()
print('Data downloaded')
# ---------------------------------------------------------------------------------------------
print('Finding available ports...')

target = socket.gethostbyname(socket.gethostname())
available_ports = []
occupied_ports = []

try:
    # Scan all ports from 5000->5050
    for port in tqdm(range(5000, 5011)):
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
port = int(input('Enter port [5000-5020] to start node: '))
while True:
    if port in available_ports:
        break

    else:
        port = int(input('ERROR: port not available, enter valid port: '))

# Gather LAN IP address of the host computer
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
time_stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

# Send a post request to the node server
requests.post('http://146.169.254.109:5050/new_node', json=(str(ip_address) + ':' + str(port), time_stamp))

for addr in db.active_nodes:
    requests.post('http://' + addr + '/new_node', json=(str(ip_address) + ':' + str(port), time_stamp))

print('Node started on port: %s' % port)
