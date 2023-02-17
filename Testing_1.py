import requests


try:
    requests.post('http://146.169.250.232:5050/mined', json={"key":"value"})

except requests.exceptions.RequestException as error:
    print(error)
    print('Peer at %s not running. Continuing to next peer.' % addr)
