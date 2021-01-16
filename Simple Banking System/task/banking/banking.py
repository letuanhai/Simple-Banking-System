import random

WELCOME_PROMPT = """
1. Create an account
2. Log into account
0. Exit
"""
LOGGED_IN_PROMPT = """
1. Balance
2. Log out
0. Exit
"""


class Account:
    accounts = {}

    # Dictionary of card_number:Account object pairs
    def __init__(self):
        card_number = "400000" + format(len(Account.accounts), "09")
        digits = []
        for i, d in enumerate(card_number):
            if i % 2 == 0:
                digits.append(2 * int(d) if 2 * int(d) <= 9 else 2 * int(d) - 9)
            else:
                digits.append(int(d) if int(d) <= 9 else int(d) - 9)
        checksum = 0 if sum(digits) % 10 == 0 else 10 - (sum(digits) % 10)
        card_number = card_number + str(checksum)
        self.card_number = card_number
        self.pin = format(random.randint(0, 9999), "04")
        self.balance = 0
        Account.accounts[card_number] = self


def create_account():
    new_account = Account()
    print(f"Your card has been created\nYour card number:\n{new_account.card_number}")
    print(f"Your card PIN:\n{new_account.pin}")


def log_in():
    card_number = input("Enter your card number:")
    pin_code = input("Enter your PIN:")
    if card_number in Account.accounts:
        if Account.accounts[card_number].pin == pin_code:
            print("You have successfully logged in!")
            return True, Account.accounts[card_number]
    print("Wrong card number or PIN!")
    return False, card_number


logged_in = False
choice = None
account_id = None
while choice != 0:
    choice = int(input(LOGGED_IN_PROMPT if logged_in else WELCOME_PROMPT))
    if not logged_in:
        if choice == 1:
            create_account()
        elif choice == 2:
            logged_in, account_id = log_in()
    else:
        if choice == 1:
            print("Balance: ", account_id.balance)
        else:
            logged_in = False

print("Bye!")
