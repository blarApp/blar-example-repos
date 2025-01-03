from bank import BankAccount, BankSystem
from utils import greet

def main():
    bank_system = BankSystem()
    
    # Create accounts
    bank_system.create_account("John Doe", 1000)
    bank_system.create_account("Jane Smith", 500)
    
    # Display greeting and initial balance
    print(greet("Welcome to the Bank!"))
    
    # Perform some transactions
    john = bank_system.get_account("John Doe")
    jane = bank_system.get_account("Jane Smith")
    
    print(f"John's balance: ${john.balance}")
    print(f"Jane's balance: ${jane.balance}")
    
    john.deposit(200)
    jane.withdraw(100)
    
    print(f"John's balance after deposit: ${john.balance}")
    print(f"Jane's balance after withdrawal: ${jane.balance}")
    
    # List all accounts
    bank_system.list_accounts()

if __name__ == "__main__":
    main()
