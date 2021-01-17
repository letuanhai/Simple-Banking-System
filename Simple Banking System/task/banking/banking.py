import random
import sqlite3

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

cur.execute("DROP TABLE card;")
cur.execute(
    "CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"
)
conn.commit()

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


def new_card(number_of_account):
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
    card_number, pin, balance = new_card(number_of_acc)
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
            print("Balance: ", account_id[3])
        else:
            logged_in = False

conn.close()
print("Bye!")
