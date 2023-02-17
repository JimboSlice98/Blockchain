class Chain(object):
    # Object that receives a list of block objects
    def __init__(self, blocks):
        self.blocks = blocks

    # Method to check if a given chain is valid
    def is_valid(self):
        """
          A chain is deemed valid only if:
          1) Each block is indexed one after the other
          2) Each block's 'prev_hash' is the hash of the previous block
          3) The block's hash is valid and meets the required difficulty
        """
        for index, cur_block in enumerate(self.blocks[1:]):
            prev_block = self.blocks[index]

            # Check point 1) Are the indexes in order
            if prev_block.index + 1 != cur_block.index:
                print('index error')
                return False

            # Check point 2) Are the has values linked
            if prev_block.hash != cur_block.prev_hash:
                print('hash error')
                return False

            # Check point 3) Is the hash of a block correct and does it meet the difficulty
            if not cur_block.is_valid():
                print('block invalid')
                return False

        return True

    # Method used to re-save and update the local blockchain by calling the save method of a given block
    def self_save(self):
        for b in self.blocks:
            b.self_save()

        return True

    # Method to return a list of dictionaries containing the attributes of each block in a given chain
    # NOTE THIS IS USED FOR THE FLASK WEB APP
    def block_list_dict(self):
        return [b.to_dict() for b in self.blocks]

    # NOT CURRENTLY USED, BUT COULD BE USED FOR TESTING
    def find_block_by_index(self, index):
        if len(self) <= index:
            return self.blocks[index]

        else:
            return False

    # NOT CURRENTLY USED, BUT COULD BE USED FOR TESTING
    def find_block_by_hash(self, hash):
        for b in self.blocks:
            if b.hash == hash:
              return b

        return False

    # NOT CURRENTLY USED, BUT COULD BE USED FOR TESTING
    def latest_block(self):
        return self.blocks[-1]

    # NOT CURRENTLY USED, BUT COULD BE USED FOR TESTING
    def max_index(self):
        # THIS IS ASSUMING A VALID CHAIN!
        return self.blocks[-1].index

    # ONLY USED IN THE TESTING SCRIPT
    def add_block(self, new_block):
        '''
          Put the new block into the index that the block is asking.
          That is, if the index is of one that currently exists, the new block
          would take its place. Then we want to see if that block is valid.
          If it isn't, then we ditch the new block and return False.
        '''
        if new_block.index > len(self):
            pass
        self.blocks.append(new_block)

        return True

    def __len__(self):
        return len(self.blocks)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for self_block, other_block in zip(self.blocks, other.blocks):
            if self_block != other_block:
              return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return len(self.blocks) > len(other.blocks)

    def __lt__(self, other):
        return len(self.blocks) < len(other.blocks)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
