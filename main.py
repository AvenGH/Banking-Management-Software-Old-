import random

import os

import modules.access_data as ad
import modules.email as me

import account_details_template as adt

from datetime import datetime

from bank_account import BankAccount

now=datetime.now()




os.system("cls")



try:


    


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
                    ad.saveData("accounts.dat",accounts)
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
