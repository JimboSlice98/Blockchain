import datetime
import pandas as pd

# Import from custom scripts
import sync
import utils


pd.options.mode.chained_assignment = None  # default='warn'


def txn_reverse():
    chain = sync.sync_local_dir()

    txn_all = chain.find_txn()
    txn_origination = txn_all.loc[txn_all['trans_type'] == 'Origination']
    txn_reversal = txn_all.loc[txn_all['trans_type'] == 'Reversal']
    txn_reversed = txn_reversal['origin_id'].tolist()

    # Dataframe containing the list of in progress transactions
    txn_pending = txn_origination[~txn_origination['id'].isin(txn_reversed)]

    # Convert expiration column to datetime format
    txn_pending['expiration'] = pd.to_datetime(txn_pending['expiration'], format='%Y-%m-%d', errors='coerce')

    # Create mask and select expired transactions
    date = pd.to_datetime(datetime.date.today())
    mask = (txn_pending['expiration'] <= date)
    txn_expired = txn_pending.loc[mask]

    # List of expired transaction ids
    expired_ids = txn_expired['id'].to_list()

    # Generate and send reversal transactions
    for id in expired_ids:
        utils.send_txn(id, reverse=True)

txn_reverse()
