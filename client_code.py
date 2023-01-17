import requests
import socket
from datetime import datetime


print('Gathering peer node data from server...')
config_PEERS = []

server_addr = 'http://localhost:5050/get_nodes'
try:
    r = requests.get(server_addr).json()

except requests.exceptions.ConnectionError:
    print('Server not reachable')

else:
    for ip_addr in r['active_nodes']:
        config_PEERS.append('http://' + ip_addr)

print(config_PEERS)

print('Data downloaded')

# print('Validating peer node addresses...')
#
# available_ports = []
# occupied_ports = []
#
# # Use websockets to check if any nodes are running on the network
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.settimeout(2)
# for port in range(5000, 5004):  # SOMEHOW MAKE THIS INCLUSIVE SO YOU KNOW WHAT PORTS
#     # Scan through listed in config.py
#     try:
#         sock.connect(('127.0.0.1', port))
#
#     except:
#         available_ports.append(port)
#
#     else:
#         sock.close()
#         occupied_ports.append(port)
#
# print('Node(s) running at: %s' % occupied_ports)
# print('Available ports at: %s' % available_ports)

# Allow user to select port to run the node
port = int(input('Enter port to run node: '))
# while True:
#     if port in available_ports:
#         break
#
#     else:
#         port = int(input('ERROR: port not available, enter valid port: '))

# Gather LAN IP address of the host computer
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
time_stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

# Send a post request to the node server
requests.post('http://146.169.252.144:5050/new_node', json=(str(ip_address) + ':' + str(port), time_stamp))

print('Node started on port: %s' % port)
