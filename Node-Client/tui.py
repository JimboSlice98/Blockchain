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
			print('Not yet defined')
			# return menu_2()


def menu_1():
	os.system('cls')
	userAnswers = menu.menu_1()

	match userAnswers['ans']:
		# Query blockchain transactions
		case 0:
			return menu_1()

		# Query user data
		case 1:
			print('Not yet defined')
			# return menu_2()

		# Back
		case 2:
			return menu_0()


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

	#
	# # -------------------------- Game End ------------------------------
	# os.system('cls')
	# display(f"     Your      Score : 5", "banner3-D")
	# time.sleep(4)

# elif ch == 'q':
# 	break

