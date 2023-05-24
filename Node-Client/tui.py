import os
import time
import pyfiglet
import pandas as pd

# Import from custom scripts
import menu
import utils
import chain
import sync


def menu_0():
	os.system('cls')
	userAnswers = menu.menu_0()

	match userAnswers['ans']:
		# Query blockchain data
		case 0:
			return menu_1()

		# Enter a new transaction
		case 1:
			return menu_2()


def menu_1():
	os.system('cls')
	userAnswers = menu.menu_1()

	match userAnswers['ans']:
		# See all transactions
		case 0:
			chain = sync.sync_local_dir()
			print(chain.find_txn())
			print('\n')

			menu.menu_back()
			return menu_1()

		# Query by transaction ID
		case 1:
			return menu_transID()

		# Query by user ID
		case 2:
			return menu_userID()

		# Back
		case 3:
			return menu_0()


def menu_2():
	os.system('cls')
	userAnswers = menu.menu_2()

	os.system('cls')

	print('Transction Details:\n')
	print('------------------')
	print(f'Lender: {userAnswers["lender"]}\n'
		  f'Borrower: {userAnswers["borrower"]}\n'
		  f'Type: {userAnswers["type"]}\n'
		  f'Security: {userAnswers["security"]}\n'
		  f'Price: {userAnswers["price"]}\n'
		  f'Variance: {userAnswers["variance"]}%\n'
		  f'Quantity: {userAnswers["quantity"]}\n'
		  f'Expiration: {userAnswers["expiration"]}')
	print('------------------\n\n')

	userAnswersNew = menu.menu_2_1()

	match userAnswersNew['ans']:
		# Yes
		case 0:
			utils.send_txn(userAnswers)
			print('Transaction submitted')
			time.sleep(1)
			print('Returning to menu...')
			time.sleep(1)
			return menu_0()

		# No
		case 1:
			menu_2()
			# return menu_2()

		# Back
		case 2:
			return menu_0()

	return


def menu_transID():
	os.system('cls')
	userAnswers = menu.menu_transID()

	chain = sync.sync_local_dir()
	print(chain.find_txn(type='transaction', key=userAnswers['trans_id']))
	print('\n')

	menu.menu_back()
	return menu_1()


def menu_userID():
	os.system('cls')
	userAnswers = menu.menu_userID()

	chain = sync.sync_local_dir()
	print(chain.find_txn(type='user', key=userAnswers['user_id']))
	print('\n')

	menu.menu_back()
	return menu_1()


# while True:
os.system('cls')
ascii_banner = pyfiglet.figlet_format('Blockchain Network Client')
print(ascii_banner)
print('Press Space to start the game, q to exit')

ch = input('')

# while True:
if ch == ' ':
	os.system('cls')
	menu_0()

# elif ch == 'q':
# 	break

