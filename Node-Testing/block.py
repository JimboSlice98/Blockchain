import hashlib
import json

# Import from custom scripts
from config import *


class Block(object):
    def __init__(self, dictionary):
        # Receives a dictionary of attribute data to store in a given block
        for key, value in dictionary.items():
            # Convert data type of attributes listed in config.py
            if key in BLOCK_VAR_CONVERSIONS:
                setattr(self, key, BLOCK_VAR_CONVERSIONS[key](value))

            else:
                setattr(self, key, value)

        # Need to add a 'hash' and 'nonce' and attributes to the genesis block only
        if not hasattr(self, 'hash'):
            self.hash = self.update_self_hash()

        if not hasattr(self, 'nonce'):
            self.nonce = 'None'

    # Method to compile a given block's attributes into a single string
    def header_string(self):
        return str(self.index) + str(self.timestamp) + self.prev_hash + self.origin + str(self.nonce) + str(self.data)

    # Method to generate a given block's header data
    def generate_header(index, timestamp, prev_hash, hash, origin, nonce, data):
        return str(index) + str(timestamp) + prev_hash + str(origin) + str(nonce) + data

    # Method to update the has attribute of a given block
    def update_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string().encode('utf-8'))
        new_hash = sha.hexdigest()
        self.hash = new_hash

        return new_hash

    # Save a given block as a single JSON file to the chaindata directory (ATTRIBUTES AS STRINGS)
    def self_save(self):
        # Ensure each JSON file consists of leading zeros
        index_string = str(self.index).zfill(6)
        filename = '%s%s.json' % (CHAINDATA_DIR, index_string)
        with open(filename, 'w') as block_file:
            json.dump(self.to_dict(), block_file)

    # Method to return the string of a given block's attributes as a dictionary
    def to_dict(self):
        info = {}
        info['index'] = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash'] = str(self.hash)
        info['origin'] = str(self.origin)
        info['nonce'] = str(self.nonce)
        info['data'] = str(self.data)

        return info

    # Method to determine if the proof of work meets the conditions stored in config.py
    def is_valid(self):
        sha = hashlib.sha256()
        sha.update(self.header_string().encode('utf-8'))
        verify_hash = sha.hexdigest()

        if not self.hash == verify_hash:
            return False

        self.update_self_hash()
        # Ensure there are the required number of leading zeros in the hash value
        if str(self.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
            return True

        else:
            return False

    def __repr__(self):
        return "Block<index: %s>, <hash: %s>" % (self.index, self.hash)

    def __eq__(self, other):
        return (self.index == other.index and
           self.timestamp == other.timestamp and
           self.prev_hash == other.prev_hash and
           self.hash == other.hash and
           self.data == other.data and
           self.nonce == other.nonce)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.timestamp < other.timestamp

    def __lt__(self, other):
        return self.timestamp > other.timestamp
