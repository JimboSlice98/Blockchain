import requests


print('Gathering node addresses from server...')

server_addr = 'http://146.169.255.151:5050'

con_err = 1
while con_err == 1:
    try:
        r = requests.get(server_addr + '/get_nodes').json()
        print(r)
        # db.active_nodes = r['active_nodes']
        # db.inactive_nodes = r['inactive_nodes']
        con_err = 0

    except requests.exceptions.ConnectionError:
        print('ERROR: Server not reachable')
        server_addr = input('Enter server address: ')
        print('Connecting to server...')
        con_err = 1

