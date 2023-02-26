import os
import json


class trans_db(object):
    def __init__(self):
        self.trans = []

    # def db_to_dict(self):
    #     data = {"trans": self.active_nodes}
    #
    #     return data

    # Method to save database to local directory
    def self_save(self):
        # Nest dictionaries to create a single object
        # data = self.db_to_dict()

        # Save data object as JSON file
        filename = 'trans_database.json'
        with open(filename, 'w') as database:
            json.dump(self.trans, database)

    # Method to populate the  database object from the local directory
    def sync_local_dir(self):
        filepath = 'trans_database.json'
        if os.path.exists(filepath):
            with open(filepath, 'r') as data_file:
                try:
                    # Read JSON database file stored in local directory
                    data = json.load(data_file)

                    self.trans = data

                except:
                    print('Local transaction database not available')
                    return False

    # def clean(self):
    #     self.sync_local_dir()
    #     time_stamp = int(datetime.utcnow().strftime('%Y%m%d%H%M'))
    #
    #     move_addr = []
    #     del_addr = []
    #
    #     # Iterate through the active node addresses and remove inactive nodes (>10 mins)
    #     for key in self.active_nodes:
    #         if time_stamp - int(self.active_nodes[key]) > 5:
    #             # Add inactive node to the inactive list
    #             self.inactive_nodes[key] = self.active_nodes[key]
    #             move_addr.append(key)
    #
    #     # Iterate through the inactive node addresses and remove dead nodes (>1 day)
    #     for key in self.inactive_nodes:
    #         # Add inactive node to the inactive list
    #         if time_stamp - int(self.inactive_nodes[key]) > 2400:
    #             del_addr.append(key)
    #
    #     # Delete inactive nodes from the active list
    #     for key in move_addr:
    #         del self.active_nodes[key]
    #
    #     # Delete dead nodes from the inactive list
    #     for key in del_addr:
    #         del self.inactive_nodes[key]
    #
    #     self.self_save()

    # def remove(self, id):
    #     # self.sync_local_dir()
    #     del self.trans[id]
    #     self.self_save()
