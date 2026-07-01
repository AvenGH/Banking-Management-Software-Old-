import random

import os

import modules.access_data as ad
import modules.email as me

import account_details_template as adt

from datetime import datetime

now=datetime.now()




os.system("cls")



try:


    class BankAccount:


        def __init__(self, name, initial_balance,email):


            existing_account_numbers=[account.account_no for account in accounts]


            
            while True:
                acc_no=str(random.randrange(10000000,100000000))
                if acc_no not in existing_account_numbers:
                    break
          

            self.account_no=acc_no
            self.balance=initial_balance
            self.sort_code="40-39-13"
            self.PIN=str(random.randrange(1000,10000))
            self.name=name
            self.email=email
            self.attempts=3
            self.blocked=False
            self.transaction_history=[]

            adt.write_account_details(self)


            with open(f"Account Details/account{self.account_no}.txt","rb") as myfile:
                file_name=myfile.name
                host_email_address="banks4usorganisation@gmail.com"
                host_password="qnqrbspxisssfoiy"
                subject="Account Details"
                data=f"Hi {self.name}, Please find your account details attached"
                subtype="txt"
                me.send_email(file_name,self.email,host_email_address,subject,data,subtype,host_password)


        def deposit(self):
            amount = float(input("Enter deposit amount: ")) 
            if not is_digit(amount):
                pass
            else:
                if amount>=0:
                    self.balance += amount
                    print(f"Deposited £{amount} Successfully")
                    self.record_transaction("Deposit",amount)
                else:
                    print("Invalid Amount")
        
        def withdraw(self):
            amount = float(input("Enter withdraw amount: "))
            if not is_digit(amount):
                pass
            else:
                if amount>=0:
                    if amount > self.balance:
                        print("Insufficient Balance.")
                    else:
                        self.balance -= amount
                        print(f"Withdrew £{amount} Successfully")
                        self.record_transaction("Withdraw",amount)
                else:
                    print("Invalid Amount")
        
        def check_balance(self):
            print(f"Your Current Balance is: £{self.balance}")
        
        def transfer(self):
            payee_acc_no=input("Enter Payee's Account Number: ")
            account2=select_account(payee_acc_no)

            if account2!=None:             
                amount = float(input("Enter transfer amount: "))
                if not is_digit(amount):
                    pass
                else:
                    if amount>=0:
                        if amount > self.balance:
                            print("Insufficient Balance.")
                        else:
                            self.balance -= amount
                            account2.balance += amount
                            print(f"Transferred £{amount} Successfully")
                            print(f"From: {self.name} To: {account2.name}")
                            self.record_transaction("Transfer",amount)
                            account2.record_transaction(f"Credit From {self.account_no}",amount)
                    else:
                        print("Invalid Amount")
            else:
                print("Account Not Found!")
        
        def change_PIN(self):

            def PIN_valid(PIN):
                try:
                    int(PIN)
                except:
                    return False
                else:
                    if len(str(PIN))==4:
                        return True

            print("Please Enter Your Current PIN")
            PIN=input()

            if self.PIN==PIN:
                while True:
                    print("Please Enter Your New PIN:")
                    new_PIN=input()
                    if PIN_valid(new_PIN):
                        print("Please Confirm Your New PIN")
                        confirm_PIN=input()
                        if new_PIN==confirm_PIN:
                            self.PIN=confirm_PIN
                            print("Successfully Changed PIN")

                            adt.write_PIN_confirmation(self)

                            with open(f"PIN Confirmations/account{self.account_no}.txt","rb") as myfile:
                                file_name=myfile.name
                                host_email_address="banks4usorganisation@gmail.com"
                                host_password="qnqrbspxisssfoiy"
                                subject="PIN confirmation"
                                data=f"Hi {self.name}, Your PIN has successfully been changed"
                                subtype="txt"
                                me.send_email(
                                    file_name,self.email,host_email_address,subject,data,subtype,host_password
                                )

                            break
                        else:
                            print("Incorrect PIN")
                    else:
                        print("PIN Must Be Exactly 4 Digits")
            else:
                print("Incorrect PIN")


        def record_transaction(self,transaction_type,amount):
            transaction = {"name": self.name, "account_number": self.account_no, "transaction_type": transaction_type, "amount": amount, "balance": self.balance}
            self.transaction_history.append(transaction)

        def view_transaction_history(self):
            print("Sorry! This option is currently not available")
            '''
            if not self.transaction_history:
                print("\nNo transactions made yet!")
            else:
                print("\nTRANSACTION HISTORY:")
                max_amount_length = max(len(locale.currency(transaction['amount'], grouping=True, symbol='')) for transaction in self.transaction_history)

                print("Name".ljust(15) + "Account Number".ljust(15) + "Transaction Type".ljust(20) + "Amount".rjust(max_amount_length + 1) + "Balance".rjust(15))
                for transaction in self.transaction_history:
                    formatted_amount = locale.currency(transaction["amount"], grouping=True, symbol='').rjust(max_amount_length)
                    print(transaction['name'].ljust(15) + transaction['account_number'].ljust(15) + transaction['transaction_type'].ljust(20) + '£' + formatted_amount + str(transaction['balance']).rjust(15))
            '''
        def close_account(self):
            print("\nPlease Enter Your PIN:")
            PIN=input()
            if PIN!=self.PIN:
                print("Invalid PIN")
            else:
                print("Closed Account Successfully")
                accounts.remove(self)
                start_menu()


    def is_digit(amt):
        try:
            float(amt)
        except:
            return False
        else:
            return True


    def create_account():

        age=input("Please Enter Your Age: ")
        if type(eval(age))!=int:
            print("Invalid Age")
        else:
            if int(age)>=18: 
                try:
                    name = input("Enter Account Name: ")
                    email=input("Enter Your Email Address: ")
                    balance = float(input("Enter Opening Balance: "))
                    account = BankAccount(name=name, initial_balance=balance, email=email)
                    accounts.append(account)
                    print(f"Account For '{name}' Created Successfully. Current Balance: £{balance}")
                except:
                    print("Invalid Details")

            else:
                print("Access Denied! Please Try Again Later")
    
    def select_account(accno):
        for account in accounts:
            if account.account_no==accno:
                return account

    def log_in():
        print("Please Enter Your Account Number: ")
        account_number=input()

        account=select_account(account_number)

        if account==None:
            print("Account Not Found!")

        elif account.blocked:
            print("Sorry! This account has been blocked")

        else:
            print("\nPlease Enter Your PIN:")
            PIN=input()
            if PIN!=account.PIN:
                print("Invalid PIN")
                account.attempts-=1
                if account.attempts>0:
                    print("We will lock your account if you continue to enter your details incorrectly")
                if account.attempts==0:
                    print("Account Blocked")
                    account.blocked=True
            else:
                return account

    def exit_program():
        print("Thank You For Banking With Us!")
        ad.saveData("accounts.dat",accounts)
        quit()
    

    def start_menu():

        def _log_in_():
            account=log_in()
            if account:   
                main_menu(account)

        def main_menu(account):
            
            main_menu_options={
                '1':account.deposit,
                '2':account.withdraw,
                '3':account.check_balance,
                '4':account.transfer,
                '5':account.change_PIN,
                '6':start_menu
            }

            while True:
                print("\nMAIN MENU:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Transfer")
                print("5. Change PIN")
                print("6. View Transaction History")
                print("7. Close Account")
                print("8. Exit")

                choice = input("\nEnter Your Option No. ")

                if choice in main_menu_options:
                    main_menu_options[choice]()    
                else:
                    print("Oops! Invalid Option...")

    
        while True:

            start_menu_options={
                '1':create_account,
                '2':_log_in_,
                '3':exit_program
            }

            print("\nWelcome to Banks4Us Online Banking!")
            print("\n1. Create an account")
            print("2. Log in to an account")
            print("3. Exit")

            choice = input("\nEnter Your Option No. ")
            print()

            if choice in start_menu_options:
                start_menu_options[choice]()
            else:
                print("Oops! Invalid Option...")

    try:
        accounts=ad.loadData("accounts.dat")
    except:
        accounts=[]

    start_menu()



except KeyboardInterrupt:
    ad.saveData("accounts.dat",accounts)

except SystemExit:
    ad.saveData("accounts.dat",accounts)
