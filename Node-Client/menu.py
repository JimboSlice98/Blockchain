from PyInquirer import prompt
from examples import custom_style_3


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
                 'choices': [{'name': 'Query blockchain transactions', 'value': 0},
                             {'name': 'Query user data', 'value': 1},
                             {'name': '↳ Back', 'value': 2}]}

    answers = prompt(questions, style=custom_style_3)
    return answers


def menu_2():
    questions = {'type': 'list',
                 'name': 'ans',
                 'message': 'Pick an option...',
                 'choices': [{'name': 'Query blockchain transactions', 'value': 0},
                             {'name': 'Query user data', 'value': 1},
                             {'name': '↳ Back', 'value': 2}]}

    answers = prompt(questions, style=custom_style_3)
    return answers