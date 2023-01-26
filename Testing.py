import requests
import socket
from datetime import datetime


hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
time_stamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

requests.post('http://localhost:5050/new_node', json=('127.0.0.1:' + str(5002), time_stamp))
