# Write your code here

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
        card_number = "400000" + format(random.randint(0, 9999999), "09")
        card_digits = []

def create_account(acc_list):
    card_number = "400000" + format(random.randint(0, 9999999), "09") + "0"
    while card_number in acc_list:
        card_number = (
            "400000"
            + format(random.randint(0, 9999999), "09")
            + str(random.randint(1, 9))
        )
    acc_list[card_number] = (format(random.randint(0, 9999), "04"), 0)
    print(f"Your card has been created\nYour card number:\n{card_number}")
    print(f"Your card PIN:\n{acc_list[card_number][0]}")
    return acc_list


def log_in(acc_list):
    card_number = input("Enter your card number:")
    pin_code = input("Enter your PIN:")
    if acc_list.get(card_number, ["a"])[0] == pin_code:
        print("You have successfully logged in!")
        return True, card_number
    else:
        print("Wrong card number or PIN!")
        return False, card_number


logged_in = False
choice = None
account_id = None
while choice != 0:
    choice = int(input(LOGGED_IN_PROMPT if logged_in else WELCOME_PROMPT))
    if not logged_in:
        if choice == 1:
            create_account(accounts)
        elif choice == 2:
            logged_in, account_id = log_in(accounts)
    else:
        if choice == 1:
            print("Balance: ", accounts[account_id][1])
        else:
            logged_in = False

print("Bye!")
