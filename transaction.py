from bank import BankAccount

def process_deposit(account: Account, amount):
    account.deposit(amount)
    print(f"Deposited ${amount}. New balance: ${account.balance}")

def process_withdrawal(account: Account, amount):
    if account.withdraw(amount):
        print(f"Withdrew ${amount}. New balance: ${account.balance}")
    else:
        print("Insufficient funds.")
