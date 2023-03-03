import ast
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

            # Convert data list string back to list
            elif key == 'data':
                if type(value) == list:
                    setattr(self, key, value)

                else:
                    setattr(self, key, ast.literal_eval(value))

            # Handling for additional attributes
            else:
                print(f'Unexpected attribute {key}: {value}')
                setattr(self, key, value)

    # Method to compile a given block's attributes into a single string
    def header_string(self):
        return str(self.index) + str(self.timestamp) + self.prev_hash + self.origin + self.merkle + str(self.nonce)

    # # Method to generate a given block's header data
    # def generate_header(index, timestamp, prev_hash, hash, origin, merkle, nonce):
    #     return str(index) + str(timestamp) + prev_hash + str(origin) + merkle + str(nonce)

    # Method to update the has attribute of a given block
    def update_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string().encode('utf-8'))
        new_hash = sha.hexdigest()
        self.hash = new_hash

        return new_hash

    def update_merkle(self):
        # Function to compute the combines value of two hashes
        def hash2(hash_a, hash_b):
            # Reverse inputs before and after hashing due to big-endian / little-endian nonsense
            combinedHash = hash_a[::-1] + hash_b[::-1]

            # Compute hash of the combined hash values
            sha = hashlib.sha256()
            sha.update(combinedHash.encode('utf-8'))
            hash = sha.hexdigest()

            return hash

        # Function to hash a pair of items recursively to find the Merkle root
        def merkle(hashList):
            if len(hashList) == 1:
                return hashList[0]

            newHashList = []
            # Create hash of pairs of values, for odd length the last is skipped
            for i in range(0, len(hashList) - 1, 2):
                newHashList.append(hash2(hashList[i], hashList[i + 1]))

            # Hash the last item twice if the list contains an odd number of items
            if len(hashList) % 2 == 1:
                newHashList.append(hash2(hashList[-1], hashList[-1]))

            return merkle(newHashList)

        if len(self.data) == 0:
            # Return the Merkel root of a blank string without computation
            merkleRoot = '0000000000000000000000000000000000000000000000000000000000000000'

        else:
            hashList = []
            for transaction in self.data:
                hashList.append(transaction['id'])

            merkleRoot = merkle(hashList)

        return merkleRoot

    # Save a given block as a single JSON file to the chaindata directory (ATTRIBUTES AS STRINGS)
    def self_save(self):
        # Ensure each JSON file consists of leading zeros
        index_string = str(self.index).zfill(6)
        filename = '%s%s.json' % (CHAINDATA_DIR, index_string)
        with open(filename, 'w') as block_file:
            json.dump(self.to_dict(), block_file)
            block_file.close()

    # Method to return the string of a given block's attributes as a dictionary
    def to_dict(self):
        info = {}
        info['index'] = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash'] = str(self.hash)
        info['origin'] = str(self.origin)
        info['merkle'] = str(self.merkle)
        info['nonce'] = str(self.nonce)
        info['data'] = str(self.data)

        return info

    # Method to determine if the proof of work meets the conditions stored in config.py
    def is_valid(self):
        sha = hashlib.sha256()
        sha.update(self.header_string().encode('utf-8'))
        verify_hash = sha.hexdigest()
        verify_merkle = self.update_merkle()

        # Check if the hash value is the correct hash of the block
        if not self.hash == verify_hash:
            return False

        # Check if the hash value meets the required difficulty
        if not str(self.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
            return False

        # Check if the Merkle root is valid to verify transactional integrity
        if not self.merkle == verify_merkle:
            return False

        else:
            return True

    def __repr__(self):
        # return "Block<index: %s>, <hash: %s>" % (self.index, self.hash)
        return f'Block: {self.index}, merkle: {self.merkle}, number txns: {len(self.data)}'

    def __eq__(self, other):
        return (self.index == other.index and
                self.hash == other.hash and
                self.nonce == other.nonce)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.timestamp < other.timestamp

    def __lt__(self, other):
        return self.timestamp > other.timestamp
