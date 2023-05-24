import hashlib
import pandas as pd

# Import from custom scripts
import chain
import sync


def txn_reverse():
    chain = sync.sync_local_dir()

    txn_all = chain.find_txn()
    txn_origination = txn_all.loc[txn_all['trans_type'] == 'Origination']
    txn_reversal = txn_all.loc[txn_all['trans_type'] == 'Reversal']
    txn_reversed = txn_reversal['origin_id'].tolist()

    # Dataframe containing the list of in progress transactions
    txn_pending = txn_origination[~txn_origination['id'].isin(txn_reversed)]

    print(txn_all)
    print()
    print(txn_origination)
    print()
    print(txn_reversal)
    print()
    print(txn_pending)

txn_reverse()
