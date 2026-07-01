class BankAccount:

    def __init__(self, name, initial_balance,email,accounts):

        import random
        import modules.access_data as ad
        

        existing_account_numbers=[account.account_no for account in accounts]
        
        while True:
            acc_no=str(random.randrange(10000000,100000000))
            if acc_no not in existing_account_numbers:
                break
        
        #ASSIGNS ATTRIBUTES TO AN OBJECT

        self.account_no=acc_no
        self.balance=initial_balance
        self.sort_code="40-39-13"
        self.PIN=str(random.randrange(1000,10000))
        self.name=name
        self.email=email
        self.attempts=3
        self.blocked=False
        self.transaction_history=[]

        


    