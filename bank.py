class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            return False

class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, owner, balance=0):
        if owner not in self.accounts:
            self.accounts[owner] = BankAccount(owner, balance)
        else:
            raise ValueError(f"Account for {owner} already exists.")

    def get_account(self, owner):
        return self.accounts.get(owner, None)

    def list_accounts(self):
        print("Account List:")
        for account in self.accounts.values():
            print(f"{account.owner}: ${account.balance}")
