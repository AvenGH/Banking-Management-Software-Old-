def write_account_details(account):
    with open(f"E:\\Python Projects\\Banking Management Software\\Account Details\\account{account.account_no}.txt","w") as myfile:
        myfile.write(
        f"""
    Dear {account.name},

    Your account has successfully been created.

    Your Default PIN Is: {account.PIN}
    Your Account Number Is: {account.account_no}
    Your Sort Code Is: {account.sort_code}

    Your Opening Balance Is: £{account.balance}

    Any other queries, please contact us on https:\\banks4us.co.uk

        """)

def write_PIN_confirmation(account):
    with open(f"PIN Confirmations\\account{account.account_no}.txt","w") as myfile:
        myfile.write(
        f"""
    Dear {account.name}, [{account.account_no}]

    Your New PIN Is: {account.PIN}

    Any other queries, please contact us on https:\\banks4us.co.uk

        """)