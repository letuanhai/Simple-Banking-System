import random
import sqlite3

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"
)
conn.commit()

WELCOME_PROMPT = """
1. Create an account
2. Log into account
0. Exit
"""
LOGGED_IN_PROMPT = """
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""

class Account:
    def __init__(self, number, pin, balance):
        self.card_number = number
        self.pin = pin
        self.balance = balance

    def check_balance(self):
        print('Balance: ', self.balance)

    def add_income(self, income):
        input('Enter income:\n')
        cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (self.card_number, income))
        conn.commit()
        self.balance += income
        print('Income was added!')

    def do_transfer(self, recipient, amount):
        if not is_valid_card(recipient):
            print('Probably you made a mistake in the card number. Please try again!')
            return False
        elif self.balance < amount:
            print('')

    def close_account(self):
        pass


def is_valid_card(card_number):
    digits = []
    for i, d in enumerate(card_number[:-1]):
        if i % 2 == 0:
            digits.append(2 * int(d) if 2 * int(d) <= 9 else 2 * int(d) - 9)
        else:
            digits.append(int(d) if int(d) <= 9 else int(d) - 9)
    checksum = sum(digits, int(card_number[-1]))
    return checksum % 10 == 0


def new_card_number(number_of_account):
    card_number = "400000" + format(number_of_account + 1, "09")
    digits = []
    for i, d in enumerate(card_number):
        if i % 2 == 0:
            digits.append(2 * int(d) if 2 * int(d) <= 9 else 2 * int(d) - 9)
        else:
            digits.append(int(d) if int(d) <= 9 else int(d) - 9)
    checksum = 0 if sum(digits) % 10 == 0 else 10 - (sum(digits) % 10)
    card_number = card_number + str(checksum)
    pin = format(random.randint(0, 9999), "04")
    balance = 0
    return card_number, pin, balance


def create_account():
    number_of_acc = cur.execute("SELECT COUNT(*) FROM card;").fetchone()[0]
    card_number, pin, balance = new_card_number(number_of_acc)
    cur.execute(
        "INSERT INTO card VALUES (?, ?, ?, ?);",
        (number_of_acc + 1, card_number, pin, balance),
    )
    conn.commit()
    print(f"Your card has been created\nYour card number:\n{card_number}")
    print(f"Your card PIN:\n{pin}")


def log_in():
    card_number = input("Enter your card number:")
    pin_code = input("Enter your PIN:")
    cur.execute("SELECT * FROM card WHERE number = ?;", (card_number,))
    account = cur.fetchone()
    if account:
        if account[2] == pin_code:
            print("You have successfully logged in!")
            return True, account
    print("Wrong card number or PIN!")
    return False, None


logged_in = False
choice = None
current_account = None
while choice != 0:
    choice = int(input(LOGGED_IN_PROMPT if logged_in else WELCOME_PROMPT))
    if not logged_in:
        if choice == 1:
            create_account()
        elif choice == 2:
            logged_in, current_account = log_in()
    else:
        if choice == 1:
            print("Balance: ", current_account[3])
        else:
            logged_in = False

conn.close()
print("Bye!")
