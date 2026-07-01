import modules.access_data as ad

try:
    accounts=ad.loadData("accounts.dat")
except:
    accounts=[]

import random

import account_details_template as adt

import modules.email as me

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

            adt.write_account_details(self)


            with open(f"Account Details/account{self.account_no}.txt","rb") as myfile:
                file_name=myfile.name
                host_email_address="banks4usorganisation@gmail.com"
                host_password="qnqrbspxisssfoiy"
                subject="Account Details"
                data=f"Hi {self.name}, Please find your account details attached"
                subtype="txt"
                me.send_email(file_name,self.email,host_email_address,subject,data,subtype,host_password)
                accounts.append(self)
                ad.saveData('accounts.dat',accounts)


        def deposit(self):
            amount = float(input("Enter deposit amount: ")) 
            if not isinstance(eval(amount),float):
                pass
            else:
                if amount>=0:
                    self.balance += amount
                    print(f"Deposited £{amount} Successfully")
                    ad.saveData('accounts.dat',accounts)
                else:
                    print("Invalid Amount")
        
        def withdraw(self):
            amount = float(input("Enter withdraw amount: "))
            if not isinstance(eval(amount),float):
                pass
            else:
                if amount>=0:
                    if amount > self.balance:
                        print("Insufficient Balance.")
                    else:
                        self.balance -= amount
                        print(f"Withdrew £{amount} Successfully")
                        ad.saveData('accounts.dat',accounts)
                else:
                    print("Invalid Amount")
        
        def check_balance(self):
            print(f"Your Current Balance is: £{self.balance}")
        
        def transfer(self):
            payee_acc_no=input("Enter Payee's Account Number: ")
            account2=self.select_account(payee_acc_no)

            if account2!=None:             
                amount = float(input("Enter transfer amount: "))
                if not isinstance(eval(amount),float):
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
                            ad.saveData('accounts.dat',accounts)
                    else:
                        print("Invalid Amount")
            else:
                print("Account Not Found!")

        def select_account(accno):
            for account in accounts:
                if account.account_no==accno:
                    return account
        
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
                            ad.saveData('accounts.dat',accounts)

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


    