from bank import BankAccount

def process_deposit(account: BankAccount, amount):
    if amount > 0:  
        temp_balance = account.balance
        account.deposit(amount)
        temp_balance = account.balance
        print(f"Deposited ${amount}. New balance: ${temp_balance}")
    else:
        print("Amount must be greater than zero.") 

def process_withdrawal(account: BankAccount, amount):
    if amount > 0:  
        if account.balance >= amount:  
            if account.withdraw(amount):
                print(f"Withdrew ${amount}. New balance: ${account.balance}")
            else:
                print("Withdrawal failed.")  
        else:
            print("Insufficient funds.")
    else:
        print("Amount must be greater than zero.")
