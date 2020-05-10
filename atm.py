import sqlite3
from random import randint

connection = sqlite3.connect("accountDb.db") 
cursor = connection.cursor()

def generate_detail(n):
    number = ''
    for i in range(n):                  
        number += str(randint(0, 9))
    number = int(number)
    return number 



class Account:
    def __init__(self,fname, lname, account_no, account_pin, account_balance, card_no):
        self.fname = fname
        self.lname = lname
        self.account_no = account_no
        self.account_pin = account_pin
        self.account_balance = account_balance
        self.card_no = card_no

    def create_account(self):
        sql_statement = f'''INSERT INTO Account_TBL VALUES("{self.fname}","{self.lname}",{self.account_no},{self.account_pin},{self.account_balance},{self.card_no});'''
        cursor.execute(sql_statement)
        connection.commit()
        print(f"Account created successfully!! \n Your account details are: \n Account No: {self.account_no} \n Account Pin: {self.account_pin} \n Card No: {self.card_no} \n")

    def check_balance(self):
        print("N"+str(self.account_balance)+".00")
    def transfer(self):
        try:
            acc_no = int(input("Enter receipient acc no:  "))
            amount = int(input("Enter amount: "))
            if amount > self.account_balance:
                print("Insufficient balance\n")
                return 0
            sql_statement = f'''SELECT account_balance FROM Account_TBL WHERE account_no = {acc_no};'''
            balance = cursor.execute(sql_statement).fetchall()
            if len(balance) == 0:
                return 0
            balance = balance[0][0]
            balance+=amount
            sql_statement = f'''UPDATE Account_TBL SET account_balance = {balance} WHERE account_no = {acc_no};'''
            cursor.execute(sql_statement)
            connection.commit()
            balance = self.account_balance-amount
            sql_statement = f'''UPDATE Account_TBL SET account_balance = {balance} WHERE account_no = {self.account_no};'''
            cursor.execute(sql_statement)
            connection.commit()
            print("\n Transfer Successful!!")
        except ValueError:
            return 0

    def withdraw(self):
        try:
            amount = int(input("Amount: "))
            if amount > self.account_balance:
                print("Insufficient Funds!")
                return 0
            balance = self.account_balance -  amount
            sql_statement = f'''UPDATE Account_TBL SET account_balance = {balance} WHERE account_no = {self.account_no};'''
            cursor.execute(sql_statement)
            connection.commit()
            print("Withdrawal Successful!")
        except ValueError:
            return 0
        




def launch_atm():
    try:
        print("Choose an option: ")
        print("1. Create Account")
        print("2. Transactions")
        print("\n \n")
        option = int(input("=>  "))
        if option>2:
            return 0
        return option
    except ValueError:
        return 0

def create_account():
    fname = input("First Name: ")
    lname = input("Last Name: ")
    try:
        fname = int(fname)
        lname = int(lname)
        try:
            if type(fname) == int or type(lname) == int:
                return 0
        except ValueError:
            pass
    except ValueError:
        pass
            
    balance = int(input("Opening Balance: "))
    account_no = generate_detail(10)
    account_pin = generate_detail(4)
    card_no = generate_detail(16)
    account = Account(fname, lname, account_no, account_pin, balance, card_no)
    account.create_account()

            

def transact_option_1():
    try:
        card_no = int(input("Card No 16 digits: "))
        account_pin = int(input("Acc Pin 4 digits: "))
    except ValueError:
        return []
    sql_statement = f'''SELECT * FROM Account_TBL WHERE card_no = {card_no} AND account_pin = {account_pin};'''
    cursor.execute(sql_statement)
    data = cursor.fetchall()
    return data
    
def transact_option_2():
    try:
        print("Choose transaction: \n 1. Check balance \n 2. Transfer \n 3. Withdraw \n")
        option = int(input("=>  "))
        return option
    except ValueError:
        return 0



def handle_transaction(option):
    if option == 0:
        while option == 0:
            print("Choose a Valid option: ")
            option = launch_atm()

    if option == 1:
        option = create_account()
        if option == 0:
            while option == 0:
                print("Enter Valid Names! \n ")
                option = create_account()

    elif option == 2:
        data = transact_option_1()
        while len(data) != 1:
            print("\nEnter valid card no!! \n")
            data = transact_option_1()
        print(f"\n {data[0][0]} {data[0][1]} \n".upper())
        account = Account(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5])
        option = transact_option_2()
        while option == 0 or option > 3:
            option = transact_option_2()
        if option == 1:
            account.check_balance()
        if option == 2:
            option = account.transfer()
            while option == 0:
                print("Enter Valid Details!! \n")
                option = account.transfer()
        if option == 3:
            option = account.withdraw()
            while option == 0:
                print("Enter valid amount: ")
                option = account.withdraw()
        

option = launch_atm()
handle_transaction(option)


connection.commit()
connection.close()  
