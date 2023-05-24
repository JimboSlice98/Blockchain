from PyInquirer import prompt
from examples import custom_style_3
from prompt_toolkit.validation import Validator, ValidationError


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


def menu_0():
    questions = {'type': 'list',
                 'name': 'ans',
                 'message': 'Pick an option...',
                 'choices': [{'name': 'Query blockchain data', 'value': 0},
                             {'name': 'Enter a new transaction', 'value': 1}]}

    answers = prompt(questions, style=custom_style_3)
    return answers


def menu_1():
    questions = {'type': 'list',
                 'name': 'ans',
                 'message': 'Pick an option...',
                 'choices': [{'name': 'See all', 'value': 0},
                             {'name': 'Query by transaction ID', 'value': 1},
                             {'name': 'Query by user ID', 'value': 2},
                             {'name': '↳ Back', 'value': 3}]}

    answers = prompt(questions, style=custom_style_3)
    return answers


def menu_2():
    questions = [{'type': 'input',
                  'name': 'lender',
                  'message': 'Enter lender information...'},

                 {'type': 'input',
                  'name': 'borrower',
                  'message': 'Enter borrower information...'},

                 {'type': 'list',
                  'name': 'type',
                  'message': 'Select security type...',
                  'choices': ['Equity', 'Debt', 'Derivative']},

                 {'type': 'input',
                  'name': 'security',
                  'message': 'Enter security information...'},

                 {'type': 'input',
                  'name': 'price',
                  'message': 'Enter current security price...'},

                 {'type': 'input',
                  'name': 'variance',
                  'message': 'Enter variance percentage...'},

                 {'type': 'input',
                  'name': 'quantity',
                  'message': 'Enter quantity...',
                  'validate': NumberValidator,
                  'filter': lambda val: int(val)},

                 {'type': 'input',
                  'name': 'expiration',
                  'message': 'Enter contract expiration date... (YYYY-MM-DD)'}]

    answers = prompt(questions, style=custom_style_3)
    return answers


def menu_2_1():
    questions = {'type': 'list',
                 'name': 'ans',
                 'message': 'Proceed?',
                 'choices': [{'name': 'Yes', 'value': 0},
                             {'name': 'No, re-enter information', 'value': 1},
                             {'name': '↳ Back', 'value': 2}]}

    answers = prompt(questions, style=custom_style_3)
    return answers


def menu_transID():
    questions = {'type': 'input',
                  'name': 'trans_id',
                  'message': 'Enter transaction ID...'}

    answers = prompt(questions, style=custom_style_3)
    return answers


def menu_userID():
    questions = {'type': 'input',
                  'name': 'user_id',
                  'message': 'Enter user ID...'}

    answers = prompt(questions, style=custom_style_3)
    return answers


def menu_back():
    questions = {'type': 'list',
                 'name': 'ans',
                 'message': 'Return to menu...',
                 'choices': [{'name': '↳ Back', 'value': 0}]}

    answers = prompt(questions, style=custom_style_3)
    return answers
