# DATA DETECTED

data = True

if data:
    # Ask user if they want to reload previous data
    while True:
        answer = input('Previous blockchain data detected, attempt to reload (Y/N)?: ')
        if answer.upper() == 'Y':
            print('Loading previous blockchain data...')
            local_chain = True
            if local_chain:
                print('Previous blockchain data loaded successfully')
                break

            else:
                print('Unable to load previous blockchain data as the files are corrupted')
                break

        elif answer.upper() == 'N':
            break
            # print('Creating 1 genesis block...')
            # # Create the first block from scratch
            # print('Genesis 1 block created')
            # break

        else:
            continue

else:
    # NO DATA DETECTED
    print('Creating genesis block...')
    # Create the first block from scratch

    print('Genesis block created')
