CHAINDATA_DIR = 'chaindata/'
NUM_ZEROS = 5

# Designate list of 5 ports available to run nodes (5000:5004)
# MAYBE MAKE DYNAMIC IN FUTURE VERSION?

server_addr = 'http://146.169.254.151:5050'

PEERS = [
    'http://localhost:5000/',
    'http://localhost:5001/',
    'http://localhost:5002/',
    'http://localhost:5003/',
    'http://localhost:5004/'
    ]

BLOCK_VAR_CONVERSIONS = {'index': int, 'nonce': int, 'hash': str, 'prev_hash': str, 'timestamp': int}

STANDARD_ROUNDS = 100000

