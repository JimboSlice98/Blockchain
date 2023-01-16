import requests
import tqdm


print('Scanning network for peer nodes:')
available_ports = []
occupied_ports = []
for port in range(5000, 5004):  # SOMEHOW MAKE THIS INCLUSIVE SO YOU KNOW WHAT PORTS
    # Check through the list of defined ports to see if any nodes are running
    peer_blockchain_url = 'http://localhost:' + str(port)
    print('Starting HTTP pool')
    try:
        print('Scanning port: %s' % port)
        r = requests.get(peer_blockchain_url)

    except requests.exceptions.ConnectionError:
        available_ports.append(port)

    else:
        occupied_ports.append(port)

print('Node(s) running at: %s' % occupied_ports)
print('Available ports at: %s' % available_ports)
