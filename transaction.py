def process_deposit(account, amount):
    account.deposit(amount)
    print(f"Deposited ${amount}. New balance: ${account.balance}")

def process_withdrawal(account, amount):
    if account.withdraw(amount):
        print(f"Withdrew ${amount}. New balance: ${account.balance}")
    else:
        print("Insufficient funds.")
