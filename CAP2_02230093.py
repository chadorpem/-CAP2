import random
import os
import string

# Constants
ACCOUNT_FILE = "accounts.txt"
# create account
class Acc:
    def __init__(self, acc_number, password, acc_type, balance=0.0):
        self.acc_number = acc_number
        self.password = password
        self.acc_type = acc_type
        self.balance = balance

    def credited(self, amount):
        self.balance += amount
        print(f"credited {amount}. New balance is {self.balance}.")

    def debited(self, amount):
        if amount > self.balance:
            print("low balance.")
        else:
            self.balance -= amount
            print(f"debited {amount}. New balance is {self.balance}.")

    def __str__(self):
        return f"{self.acc_number},{self.password},{self.acc_type},{self.balance}"

class PersonalAcc(Acc):
    def __init__(self, acc_number, password, balance=0.0):
        super().__init__(acc_number, password, "Personal", balance)

class BusinessAcc(Acc):
    def __init__(self, acc_number, password, balance=0.0):
        super().__init__(acc_number, password, "Business", balance)

class Bank:
    def __init__(self):
        self.acc = {}
        self.load_acc()

    def load_acc(self):
        if os.path.exists(ACCOUNT_FILE):
            with open(ACCOUNT_FILE, 'r') as file:
                for line in file:
                    acc_number, password, acc_type, balance = line.strip().split(',')
                    balance = float(balance)
                    if acc_type == "Personal":
                        acc = PersonalAcc(acc_number, password, balance)
                    else:
                        acc = BusinessAcc(acc_number, password, balance)
                    self.acc[acc_number] = acc

    def save_acc(self):
        with open(ACCOUNT_FILE, 'w') as file:
            for acc in self.acc.values():
                file.write(str(acc) + "\n")

    def create_acc(self, acc_type):
        acc_number = ''.join(random.choices(string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if acc_type == "Personal":
            acc = PersonalAcc(acc_number, password)
        else:
            acc = BusinessAcc(acc_number, password)
        self.acc [acc_number] = acc
        self.save_acc()
        print(f"Account created. Account Number: {acc_number}, Password: {password}")

    def login(self, acc_number, password):
        acc = self.acc.get(acc_number)
        if acc and acc.password == password:
            print("Successfully login.")
            return acc
        else:
            print("either account number or password is invalid.")
            return None

    def delete_acc(self, acc_number):
        if acc_number in self.acc:
            del self.acc[acc_number]
            self.save_acc()
            print("Account removed.")
        else:
            print("Account not found.")

    def transfer(self, from_acc, to_acc_number, amount):
        to_acc = self.acc.get(to_acc_number)
        if not to_acc:
            print("uncliamed funds.")
            return
        if from_acc.balance < amount:
            print("low balance.")
            return
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        self.save_acc()
        print(f"Transferred {amount} to account {to_acc_number}.")

def main():
    bank = Bank()
    while True:
        print("\nBank Menu:")
        print("1. Create Personal Account")
        print("2. Create Business Account")
        print("3. Login")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            bank.create_acc("Personal")
        elif choice == '2':
            bank.create_acc("Business")
        elif choice == '3':
            acc_number = input("Enter account number: ")
            password = input("Enter password: ")
            acc = bank.login(acc_number, password)
            if acc:
                while True:
                    print("\nAccount Menu:")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer")
                    print("4. Delete Account")
                    print("5. Logout")
                    acc_choice = input("Enter choice: ")

                    if acc_choice == '1':
                        amount = int(input("Enter amount to deposit: "))
                        acc.deposit(amount)
                        bank.save_acc()
                    elif acc_choice == '2':
                        amount = int(input("Enter amount to withdraw: "))
                        acc.withdraw(amount)
                        bank.save_acc()
                    elif acc_choice == '3':
                        to_acc_number = input("Enter the account number to transfer to: ")
                        amount = int(input("Enter amount to transfer: "))
                        bank.transfer(acc, to_acc_number, amount)
                    elif acc_choice == '4':
                        bank.delete_acc(acc.acc_number)
                        break
                    elif acc_choice == '5':
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
