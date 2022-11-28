available_ports = [5000, 5001, 5002, 5003]

port = int(input('Enter port to run node: '))
while True:
    if port in available_ports:
        break

    else:
        port = int(input('ERROR: port not available, enter valid port: '))

print('Node started on port: %s' % port)
