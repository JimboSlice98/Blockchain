import os
import json


class user_db(object):
    def __init__(self):
        self.users = []

    # def db_to_dict(self):
    #     data = {"trans": self.active_nodes}
    #
    #     return data

    # Method to save database to local directory
    def self_save(self):
        # Nest dictionaries to create a single object
        # data = self.db_to_dict()

        # Save data object as JSON file
        filename = 'user_database.json'
        with open(filename, 'w') as database:
            json.dump(self.users, database)

    # Method to populate the  database object from the local directory
    def sync_local_dir(self):
        filepath = 'user_database.json'
        if os.path.exists(filepath):
            with open(filepath, 'r') as data_file:
                try:
                    # Read JSON database file stored in local directory
                    data = json.load(data_file)

                    self.users = data

                except:
                    print('Local user database not available')
                    return False

        if self.users == []:
            self.users = [{'user_id': 'Big Jim',
                           'transactions': []}]

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
    #
    def add_users(self, valid_txns):
        self.sync_local_dir()
        for txn in valid_txns:
            # Add user if the lender is not in database
            if not txn['lender'] in [user['user_id'] for user in self.users]:
                self.users.append({'user_id': txn['lender'],
                                   'transactions': [txn['id']]})

            # Add user if the borrower is not in database
            if not txn['borrower'] in [user['user_id'] for user in self.users]:
                self.users.append({'user_id': txn['borrower'],
                                   'transactions': [txn['id']]})

            # Update transaction list if the lender and borrower are known users
            for user in self.users:
                if user['user_id'] == txn['lender']:
                    user['transactions'] = [*user['transactions'], txn['id']] if txn['id'] not in user['transactions'] else user['transactions']

                if user['user_id'] == txn['borrower']:
                    user['transactions'] = [*user['transactions'], txn['id']] if txn['id'] not in user['transactions'] else user['transactions']

        self.self_save()
        print(self.users[:])

        # self.users = []



        # self.trans = [txn for txn in self.trans if txn not in valid_txns]
        # print(f'Validated transactions: {valid_txns}')
        # print(f'Remaining transactions: {self.trans}')


