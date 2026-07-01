import modules.email as me
import account_details_template as adt

def is_digit(amt):
    try:
        float(amt)
    except:
        return False
    else:
        return True

def deposit(self):
    amount = float(input("Enter deposit amount: ")) 
    if not is_digit(amount):
        pass
    else:
        if amount>=0:
            self.balance += amount
            print(f"Deposited £{amount} Successfully")
            record_transaction(self,"Deposit",amount)
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
                record_transaction(self,"Withdraw",amount)
        else:
            print("Invalid Amount")

def check_balance(self):
    print(f"Your Current Balance is: £{self.balance}")

def transfer(self,accounts):
    payee_acc_no=input("Enter Payee's Account Number: ")
    account2=select_account(payee_acc_no,accounts)

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
                    record_transaction("Transfer",amount)
                    record_transaction(account2,f"Credit From {self.account_no}",amount)
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

                    with open(f"PIN Confirmations/account{self.account_no}.txt") as myfile:
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

        # Print the transaction history table with pound sign
        print("Name".ljust(15) + "Account Number".ljust(15) + "Transaction Type".ljust(20) + "Amount".rjust(max_amount_length + 1) + "Balance".rjust(15))
        for transaction in self.transaction_history:
            formatted_amount = locale.currency(transaction["amount"], grouping=True, symbol='').rjust(max_amount_length)
            print(transaction['name'].ljust(15) + transaction['account_number'].ljust(15) + transaction['transaction_type'].ljust(20) + '£' + formatted_amount + str(transaction['balance']).rjust(15))
    '''

def select_account(accno,accounts):
    for account in accounts:
        if account.account_no==accno:
            return account