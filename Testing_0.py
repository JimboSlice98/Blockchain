data = [{'id': 'a48f5d3eaf5567debc43f3986c1dec16908c2ab0b48713d9eaf07ebdfb609d8e', 'lender': 'Jennifer Burr', 'borrower': 'Lance Scott', 'type': 'equity', 'security': 'DQE Inc.', 'quantity': 89, 'price': 327, 'strike': 344, 'expiration': '2023-5-8'}, {'id': 'de37d98ff4c5b1c352045fd5cda259585bcaf067e408a9228ff82f2035b2f0a5', 'lender': 'Johnny Flores', 'borrower': 'Tammie Serasio', 'type': 'equity', 'security': 'Legg Mason Inc.', 'quantity': 97, 'price': 158, 'strike': 176, 'expiration': '2026-3-17'}, {'id': '6a56da731c697aa8797a98edca87415836624f5799968d2a9024c250496a30fc', 'lender': 'Connie Yousef', 'borrower': 'Florence Cervantes', 'type': 'equity', 'security': 'Humana Inc.', 'quantity': 18, 'price': 27, 'strike': 42, 'expiration': '2024-11-12'}]

users = [{'user_id': 'Big Jim', 'transactions': [1, 3]},
         {'user_id': 'Jimbo', 'transactions': [1, 2]}]

users = {'user_id': 'Jimbo', 'transactions': [1, 2]}

# for txn in data:
#     print(txn)
#     if not txn['lender'] in [id for id in users['user_id']]:
#         print(txn['lender'])

print(users)

users = {key: val for key, val in ([('trans_id', 0)] + list(users.items()))}

print(users)
# users[0]['transactions'] = [*users[0]['transactions'], new_txn] if new_txn not in users[0]['transactions'] else users[0]['transactions']
#
# print(users)
