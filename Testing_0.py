data = {'key_1': '1',
        'key_2': '2',
        'key_3': '3'}

key = 'key_1'

print(data)

if key in data:
    del data[key]

print(data)
