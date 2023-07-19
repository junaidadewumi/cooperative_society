import time
import random
import mysql.connector as connection
myconn = connection.connect(host = "127.0.0.1", user = " ", passwd = " ", database = "cooperative_society")
cursor = myconn.cursor()

#def reg allows user to select the kind of registration he/she want to perform.
def reg():
    print("""
    1. Members Registration
    2. Loanee Registration
    3. Home page
    """)
    decision = input(">>> ")
    if decision == "1":
        create_members_account()                        #this function lead to registration of members
    elif decision == "2":
        create_loanee_account()                         #this function lead to registration of non - members
    elif decision == "3":
        from Homepage import homepage
        homepage()                                      #this function will take you back to homepage
    else:
        print("Incorrect, Try again!")
        reg()


# account created for members of the association
def create_members_account():
    val = []
    info = ("First_name", "middle_name", "Last_name", "Contact", "Age", "Email", "Pswd", "Address",
            "Member_id", "Contribution", "Interest", "Loan", "Status")
    querry = """INSERT INTO member(First_name, Middle_name, Last_name, Contact, Age, Email, Pswd,
    Address, Member_id, Contribution, Interest, Loan, Status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    Member_id = random.randrange(4001, 6000)        #member_id is generated randomly here
    for details in range (13):
        if info[details] == "Member_id":
            user = Member_id
        elif info[details] == "Contribution":            #contribution, loan, refund, and interest shall be zero (0), 'cause its a registration.
            user = 0                                      
        elif info[details] == "Loan":
            user = 0
        elif info[details] == "Status":
            user = 0
        elif info[details] == "Interest":
            user = 0
        else:
            user = input(f"Enter your {info[details]}: ")
        val.append(user)
    cursor.execute(querry,val)
    myconn.commit()
    time.sleep(1)
    print("""Dear user, you have been successfully registered as JCS member. Enter 1 to log in,
          2 to go back home.""")            #this print shows that the registration is successful
    time.sleep(1)
    decision = input(">>> ")
    if decision == "1":
        from loginpage import log_in
        log_in()                            #members can log in via this function to perform operation
    elif decision == "2":
        reg()                               #members can go back home after registration.


#account created for NON MEMBERS of the association
def create_loanee_account():
    val = []
    info = ("First_name", "middle_name", "Last_name", "Contact", "Age", "Email", "Pswd", "Address",
            "User_id", "Loan", "Status")
    querry = """INSERT INTO non_member(First_name, Middle_name, Last_name, Contact, Age, Email, Pswd,
    Address, User_id, Loan, Status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    User_id = random.randrange(7001, 9000)          #non - members or loanee user_id is generated randomly here.
    for details in range (11):
        if info[details] == "User_id":
            user = User_id
        elif info[details] == "Loan":               # loan and refund shall be zero (0), 'cause its a registration.
            user = 0
        elif info[details] == 'Status':
            user = 0
        else:
            user = input(f"Enter your {info[details]}: ")
        val.append(user)
    cursor.execute(querry,val)
    myconn.commit()
    time.sleep(1)
    print(f"""Dear user, your account has been created. Enter 1 to log in,
          2 to go back home.""")                                    #this print shows that the registration is successful.
    time.sleep(1)
    decision = input(">>> ")
    if decision == "1":
        from loginpage import loanee_log_in
        loanee_log_in()                                         # users can log in via this function to perform operation
    elif decision == "2":
        reg()                                               # users can go back home after registration.