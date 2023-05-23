import os
import time
import pyfiglet

# Import from custom scripts
import menu


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
		# Query blockchain transactions
		case 0:
			print('Not yet defined')
			# return menu_1()

		# Query user data
		case 1:
			print('Not yet defined')
			# return menu_2()

		# Back
		case 2:
			return menu_0()


def menu_2():
	os.system('cls')
	userAnswers = menu.menu_2()

	os.system('cls')

	print('Transction Details:')
	print(f'Lender: {userAnswers["lender"]}\n'
		  f'Borrower: {userAnswers["borrower"]}\n'
		  f'Security type: {userAnswers["type"]}\n'
		  f'Price: {userAnswers["price"]}\n'
		  f'Quantity:{userAnswers["quantity"]}\n'
		  f'Expiration: {userAnswers["expiration"]}')

	userAnswers = menu.menu_2_1()

	match userAnswers['ans']:
		# Yes
		case 0:
			print('Not yet defined')
			# return menu_1()

		# No
		case 1:
			menu_2()
			# return menu_2()

		# Back
		case 2:
			return menu_0()

	return


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

