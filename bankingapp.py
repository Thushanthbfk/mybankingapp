#import some modules 

import random
import string
import datetime
#account creation function============================================
#generate the user name
def generate_username(lname):
    strnum = ''.join(random.choices(string.digits, k=4))
    username = lname.lower().replace(" ", "") + strnum
    return username

def account_creation():
    print("================== Create a New Account =======================")
    fname = input("Enter your First Name: ")
    lname = input("Enter your Last Name: ")
    nic_num = input("Enter your NIC number: ")
    dob = input("Enter your Date of Birth (YYYY-MM-DD): ") 
    contact_num = input("Enter your Contact Number: ")

    #generate the account number  

    acc_num = random.randint(100000, 999999)
    print(" Your Account Number is:", acc_num)
    print(" Do not forget your account number!")

    username = generate_username(lname)
    print(" Your Username is:", username)
    print(" Do not forget your username!")

    creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #Save the account details in accounts text file
    with open("accounts.txt", "a") as file:
        file.write(f"{acc_num},{fname},{lname},{nic_num},{dob},{contact_num},{username},{creation_date}\n")

    print(" Account created and saved successfully!")
    #Create the balance file for new account creation
    with open("balance.txt", "a") as bfile:
        bfile.write(str(acc_num) + ",0.0\n")



#deposit======================================================================

def deposit():
    acc_num = input("Enter your account number: ")
    
    try:
        deposit_amount = float(input("Enter the amount to deposit: "))
        if deposit_amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print(" Invalid amount.")
        return

    #Read the accounts and match the correct account
    try:
        with open("accounts.txt", "r") as acc_file:
            lines = acc_file.readlines()
    except FileNotFoundError:
        print(" No account records found.")
        return

    #Read every line and choose the matching account number
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) >= 1 and parts[0] == acc_num:
            break
    else:
        #account number dis match
        print(" Account number not found.")
        return

    #Read balance file
    balances = {}
    try:
        with open("balance.txt", "r") as bal_file:
            for line in bal_file:
                acct, bal = line.strip().split(",")
                balances[acct] = float(bal)
    except FileNotFoundError:
        pass  

    
    if acc_num in balances:
        current_balance = balances[acc_num]
    else:
        print(f"Account {acc_num} does not exist. Please create an account first.")
        return  

    new_balance = current_balance + deposit_amount
    balances[acc_num] = new_balance


    # write balance
    with open("balance.txt", "w") as bal_file:
            for acct in balances:
                bal = balances[acct] #account number key to write balance using dictionery
                bal_file.write(f"{acct},{bal}\n")
    

    #for view the transaction history update transaction file
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("transactions.txt", "a") as tfile:
        tfile.write(acc_num + ",deposit," + str(deposit_amount) + "," + time + "\n")


    print(f"{deposit_amount} deposited.")
    print(f"LKR New balance for account {acc_num}: LKR{new_balance}")

#withdraw============================================================================

def withdraw():
    acc_num = input("Enter your account number: ")
    
    #check amount validation
    try:
        withdraw_amount = float(input("Enter the amount to withdraw: "))
        if withdraw_amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return
    except ValueError:
        print(" Invalid amount entered.")
        return

    #check account validation
    try:
        with open("accounts.txt", "r") as acc_file:
            lines = acc_file.readlines()
    except FileNotFoundError:
        print(" No account records found.")
        return


     #check the entered account number match or dismatch
    for line in lines:
        fields = line.strip().split(",")
        if len(fields) > 0 and fields[0] == acc_num:
            break
    else:
        print(" Account number not found.")
        return

    #Read balances
    balances = {}
    try:
        with open("balance.txt", "r") as bal_file:
            for line in bal_file:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    acct = parts[0]
                    bal = float(parts[1])
                    balances[acct] = bal
    except FileNotFoundError:
        print("Balance file not found. Nothing to withdraw.")
        return

    #Check the balance and withdraw
    if acc_num in balances:
        current_balance = balances[acc_num]
        if current_balance < withdraw_amount:
            print("Insufficient balance.")
            return
        new_balance = current_balance - withdraw_amount
        balances[acc_num] = new_balance
    else:
        print(" No balance found for this account.")
        return

    #Write updated balances
    with open("balance.txt", "w") as bal_file:
        for acct in balances:
            bal = balances[acct]
            bal_file.write(f"{acct},{bal}\n")

    print(f"{withdraw_amount} withdrawn successfully.")
    print(f"Remaining balance: {new_balance}")
 

    # save the transaction file
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("transactions.txt", "a") as tfile:
        tfile.write(acc_num + ",withdraw," + str(withdraw_amount) + "," + time + "\n")


#check balance==================================================================

def check_balance():
        acc_num = input("Enter your account number: ")

        #account validation
        try:
            with open("accounts.txt", "r") as acc_file:
                lines = acc_file.readlines()
        except FileNotFoundError:
            print("No account file found.")
            return


        #check account number validation
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) > 0 and parts[0] == acc_num:
                break
        else:
            print("Account number not found.")
            return

        #Read balance
        try:
            with open("balance.txt", "r") as bal_file:
                for line in bal_file:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        acct = parts[0]
                        bal = parts[1]
                        if acct == acc_num:
                            print(f"Current balance for account {acc_num} is LKR{bal}")
                            return
        except FileNotFoundError:
            print("Balance file not found.")
            return

        
        print("Balance record not found for this account. Possibly LKR0.00.")



#transaction history============================================
def transaction_history():
    acc_num = input("Enter your account number: ")


    #check file and history
    try:
        with open("transactions.txt", "r") as tfile:
            lines = tfile.readlines()
    except FileNotFoundError:
        print("No transaction history found.")
        return


    #create a list and append transaction details from transaction file
    matching = []

    for line in lines:
        everyindex= line.strip().split(",")
        if len(everyindex) == 4 and everyindex[0] == acc_num:
            matching.append(everyindex)

    if len(matching) == 0:
        print("No transactions found for this account.")
        return

    print("\nTransaction History for Account " + acc_num)
    print("--------------------------------------------")
    print("Account\t\tType\t\tAmount\t\tTime")
    print("--------------------------------------------")

    for trans in matching:
        account = trans[0]
        transaction_type = trans[1]
        amount = "LKR"+ trans[2]
        time = trans[3]

        print(account + "\t" + transaction_type + "\t\t" + amount + "\t\t" + time)



#Menu==========================================================================
def mainmenu():

    while True:
        print("-------------Welcome to our banking app------------")
        print("1.Create an account----------- press 1")
        print("2.Deposit money ---------------press 2")
        print("3.Withdraw money-------------- press 3")
        print("4.Check balance ---------------press 4")
        print("5.Transaction History--------- press 5")
        print("6.Exit------------------------ press 6")
        press=int(input("Press : "))
        if press==1:
            account_creation()
        elif press==2:
            deposit()
        elif press==3:
            withdraw()
        elif press==4:
            check_balance()
        elif press==5:
            transaction_history()
        else:
            exit()
 


#login===========================================================


#admin======================================================================
def admin():
    code = 30000
    password=int(input("Enter password: "))
    if code == password:
        print("================Account details=======================")
        with open ("accounts.txt","r") as accountread_file:
            account_details=accountread_file.readlines()
            print(account_details)

        print("===================Balance Details=====================")
        with open ("balance.txt","r") as balance_read_file:
            balance_details=balance_read_file.readlines()
            print(balance_details)


        print("====================Transactions====================")
        with open ("transactions.txt","r") as trans_file:
            trans_details=trans_file.readlines()
            print(trans_details)

    else:
        print("Can not Enter wrong password")

        
#inter face=====================================================       
while True:
    print("===============Welcome our banking app======================")


    print("1.USER")
    print("2.ADMIN")
    options=int(input("Press option 1 or 2 : "))
    if options==1:
        mainmenu()
    elif options==2:
        admin()
    else: 
        print("Please enter 1 or 2 only")