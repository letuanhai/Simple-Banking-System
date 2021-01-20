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
    def __init__(self, id, number, pin, balance):
        self.id = id
        self.card_number = number
        self.pin = pin
        self.balance = balance

    def check_balance(self):
        print("Balance:", self.balance)

    def add_income(self):
        income = int(input("Enter income:\n"))
        cur.execute(
            "UPDATE card SET balance = balance + ? WHERE number = ?;",
            (income, self.card_number),
        )
        conn.commit()
        self.balance += income
        print("Income was added!")

    def do_transfer(self):
        recipient = input("Transfer\nEnter card number:\n")
        if recipient == self.card_number:
            print("You can't transfer money to the same account!")
            return False
        if not is_valid_card(recipient):
            print("Probably you made a mistake in the card number. Please try again!")
            return False
        if not is_account_existed(recipient):
            print("Such a card does not exist.")
            return False
        amount = int(input("Enter how much money you want to transfer:\n"))
        if self.balance < amount:
            print("Not enough money!")
            return False
        cur.execute(
            "UPDATE card SET balance = balance + ? WHERE number = ?;",
            (amount, recipient),
        )
        cur.execute(
            "UPDATE card SET balance = balance - ? WHERE number = ?;",
            (amount, self.card_number),
        )
        conn.commit()
        self.balance -= amount
        print("Success!")

    def close_account(self):
        cur.execute("DELETE FROM card WHERE number = ?;", (self.card_number,))
        conn.commit()
        print("The account has been closed!")


def is_account_existed(card_number):
    cur.execute("SELECT * FROM card WHERE number = ?;", (card_number,))
    account = cur.fetchone()
    return bool(account)


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
            return True, Account(*account)
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
            current_account.check_balance()
        elif choice == 2:
            current_account.add_income()
        elif choice == 3:
            current_account.do_transfer()
        elif choice == 4:
            current_account.close_account()
            logged_in = False
        else:
            logged_in = False

conn.close()
print("Bye!")
