import time
import mysql.connector as connection
myconn = connection.connect(host = "127.0.0.1", user = " ", passwd = " ", database = "cooperative_society")
cursor = myconn.cursor()

#LOG IN CHECK FOR BOTH MEMBER AND NON - MEMBER
def log():
    print("""Enter
    1. member
    2. non - member
             """)
    decide = input(">>> ")
    if decide == "1":
        log_in()                            #this function lead to members log in page
    elif decide == "2":
        loanee_log_in()                     #this function lead to non - members/ loanee log in page
    else:
        print("Invalid input.")
        log()

#this line of codes cross-check the password if it is correct with the one registered on database
def checkpassword():
    global password
    print(f"Enter your password")
    password = input(">>> ")
    if password == password:
        return
    else:
        print(f"Invalid password! Try Again")
        checkpassword()


#LOG IN PAGE FOR MEMBERS
def log_in():
    global memb_password
    global memb_username
    memb_username = input("Enter your member_id: ")
    time.sleep(1)
    memb_password = input("Enter your password: ")
    val = (memb_username, memb_password)
    querry = "SELECT * from member where Member_id = %s and Pswd = %s"     # member_id and password is required here and it will be verified,
    cursor.execute (querry, val)                                          # on the member table on database where the members  input were stored.
    result = cursor.fetchone()
    time.sleep(1)
    if result:
        time.sleep(2)
        print(f"you have successfully log in as {result[1]} {result[2]} {result[3]}")   #the member details will be fetched and name will appeared after a successful log in
    else:
        print("invalid input, re - check your details and log in again ")       #the print will shows if you enter wrong details.
        log_in()
    time.sleep(2)
    print("Dear Member, Welcome to Junaid Cooperative Society (JCS). Which of service would you like to use?")
    time.sleep(1)                               #this print is the operation you can perform as members
    print("""Enter 
    1. to make contribution
    2. to take on loan 
    3. to refund the loan
    4. to go homepage
    """)
    decision = input(">>> ")
    if decision == "1":
        contribution()
    elif decision == "2":
        loan()
    elif decision == "3":
        refund_loan()
    elif decision == "4":
        from Homepage import homepage
        homepage()
    else:
        print("Errorneous! Retry!!!")


#LOG IN PAGE FOR NON - MEMBERS
def loanee_log_in():
    global password
    global username
    username = input("Enter your user_id: ")
    time.sleep(1)
    password = input("Enter your password: ")
    val = (username, password) 
    querry = "SELECT * from non_member where User_id = %s and Pswd = %s"                # user_id and password is required here and it will be verified on the non - member table on database where the users input were stored.
    cursor.execute (querry, val)
    result = cursor.fetchone()
    time.sleep(1)
    if result:
        time.sleep(2)
        print(f"you have successfully log in as {result[1]} {result[2]} {result[3]}")           #the user details will be fetched and name will appeared after a successful log in
    else:
        print("invalid input, re-check and log in again ")                                  #the print will shows if you enter wrong details.
        loanee_log_in()
    time.sleep(2)
    print("Dear User, Welcome to Junaid Cooperative Society (JCS).")  #this print is the operation you can perform as users
    time.sleep(1)
    print(""""Enter
    1. to take on loan
    2. to refund the loan
    3. to go back home
          """)
    decision = input(">>> ")
    if decision == "1":
        loan()
    elif decision == "2":
        refund_loan()
    elif decision == "3":
        from Homepage import homepage
        homepage()
    else:
        print("Errorneous! Retry!!!")
        loanee_log_in()


#CONTRIBUTION PAGE (MEMBERS ONLY)
def contribution():
    print(" Dear member, you shall have (10%) of any amount contributed to the Association.")
    time.sleep(1)
    amount = int(input("Enter amount to contribute "))
    val = (memb_username, memb_password)
    querry = "SELECT * from member where Member_id = %s and Pswd = %s"
    cursor.execute(querry, val)
    result = cursor.fetchone()
    time.sleep(1)
    if result:
            print(f"You are making a contribution to the Association acoount as {result[1]} {result[2]} {result[3]}")
            time.sleep(1)
            print("your transaction is being processing...")
            time.sleep(2)
            print(f"You have succesfully deposit {amount} into the JCS Treasure account.")
            interest = 10           #the ineterst a member will have for making contribution to the association.
            percentage = 100            #the amount contributed will be divided with the percentage.
            div = amount / percentage * interest                # div is the variable holding interest and percentage.
            new_bal = result[11] + div                  #result at index 11 is the interest column on database
            newbal = (new_bal, memb_username, memb_password)
            newquerry = "UPDATE member SET Interest = %s where Member_id = %s and Pswd = %s"        #this line of code will update interest column.
            cursor.execute(newquerry, newbal)
            Contribution = amount + result[10]                  #result at index 10 is the contribution column on database
            newval = (Contribution, memb_username, memb_password)
            qery1 = "UPDATE member SET Contribution = %s where Member_id = %s and Pswd = %s"         #this line of code will update contribution column.
            cursor.execute(qery1, newval)
            myconn.commit()
            query = "SELECT * from treasures where ID = %s"   #this line of code is selecting from society table created for treasure and profit only.
            val1 = (1, )
            cursor.execute(query, val1)
            result = cursor.fetchone()
            if result:
                newvalue = result[1] + amount
                newquery = "UPDATE treasures SET JCS_Treasure = %s where ID = %s"  #this line of code add up all the contribution maked into society trasure column.
                val3 = (newvalue, 1)
                cursor.execute(newquery, val3)
                myconn.commit()

    else:
        print("You aren't a registered member")
        from Homepage import homepage
        homepage()


#LOAN PAGE FOR BOTH MEMBERS AND NON - MEMBERS
#check if client is taking loan as member or as non member
def loan():
    print("Welcome to Junaid Cooperative Society (JCS) Loan Page!")
    time.sleep(1)
    client = input("Enter 1 as a member, 2 as NON member: ")
    if client == "1":
        member_loan()                                       #this function lead to page members can take on loan.
    elif client == "2":
        non_member_loan()                                   #this function lead to page non - members / users can take on loan.
    else:
        print("Errorneous, retry!")
        loan()


#MEMBERS WILL HAVE ACCESS TO LOAN HERE
def member_loan():
    global Contribution
    global Member_id
    Member_id = input("Enter your member id: ")         #asking for member ID is to verified member identity.
    value = (Member_id, )
    query = "SELECT * from member where Member_id = %s"         #this line of code will cross check if you are a registered member or not.
    cursor.execute(query, value)
    result = cursor.fetchone()
    if result:
        access = result[12]             #this line of code will check if you have reach your amount of limitation to borrow in a specified period.
        if access == 1000000:                   #result 12 is the loan column
            print("You have reached your amount to take on loan for the next six month.")
            log_in()
        elif access < 1000000:
            print("Please wait, lets validate your request... ")
            time.sleep(1)
        debt = result[13]               #this line of code will check if you owe money. if you owe, you will be denied to take on another loan.
        if debt > 0:
            print("Dear, member, your access to take on loan denied! Kindly clear off your debt!")
            refund_loan()
        elif debt == 0:         #this line of code will proceed with your request if you do not owe money.
            print(f"You want to take loan as {result[1]} {result[2]} {result[3]}")
            time.sleep(1)
            print("Dear member, kindly go through our Loan Application Rules before embarking on it. Thank you!")
            time.sleep(1)          #this print is few rules created for the association to have access to take on loan.
            print("""
                        JCS RULES ON LOAN (APPLICABLE TO MEMBERS ONLY)
            1. You must be a member of the JCS Association.
            2. Members with contribution have access to take on loan up to One Million Naira (# 1,000,000).
            3. Members with NO contribution have access to take on loan up to Five Hundred Thousand Naira (# 500,000).
            4. Member with contribution, the interest of the loan taken shall be two percent (2%) of the amount.
            5. Member with NO contribution, the interest of the loan taken shall be five percent (5%) of the amount.
            6. A partial amortization is not allowed. We accept a full amortization ONLY.
            7. You have ACCESS to take amount of your limition on loan in SIX MONTH!
            8. Kindly abide by the rules dear esteem member!
            """)
            time.sleep(1)
            Contribution = result[10]           #result 10 is contribution column on database.
            if Contribution > 0:                #this line of code will check if you have contribution with the association or not.
                print("Dear Esteem Member, you have access to take on loan up to One Million Naira (# 1,000,000)")              #this line of code is your access and limitation as a member who have contribution.
                time.sleep(1)
                amount = int(input(" Enter amount you want to borrow: "))
                if amount > 1000000:        #it will check if amount input is greater than your limitation.
                    print("you do not have access to this amount. Your limitation is One Million. Retry!")  #you will be deny if your amount is greater than limitation.
                    member_loan()
                elif amount <= 1000000:             #you can proceed with your request if you are within amount limitation.
                    print("please wait, your request is being process..")
                    new_querry = "SELECT * from treasures where ID = %s"        #the society treasure account will be call on here.
                    new_val = (1, )
                    cursor.execute(new_querry, new_val)
                    result2 = cursor.fetchone()
                    newbal = result2[1] - amount                # loan will be deducted from the trasure account via this line of code.
                    time.sleep(1)
                    print(f"You have been successfully granted {amount} of loan from Junaid Cooperative Society. Thank you")
                    qury = "UPDATE treasures SET JCS_Treasure = %s where ID = %s"       #treasure will be update after laon is deducted.
                    val3 = (newbal, 1)
                    cursor.execute(qury, val3)
                    myconn.commit()
                    val1 = result[12] + amount              #loan column will be updated with the amount taken.
                    qu = "UPDATE member SET Loan =%s where Member_id = %s" 
                    val4 = (val1, Member_id)
                    cursor.execute(qu, val4)
                    myconn.commit()
                    interest = 2                                    #interest expected to be added to the loan when paying back.
                    percentage = 100
                    div = amount / percentage * interest
                    refund = amount + div + result[13]                      #amount expected to refund when paying back the loan.
                    querry = "UPDATE member SET Status =%s where Member_id = %s"
                    value = (refund, Member_id)
                    cursor.execute(querry, value)
                    myconn.commit()
            elif Contribution <=0:          #this line of code shows that the member does not have contribution with the association.
                print("Dear Member, you have access to take on loan up to Five Hundred Thousand Naira (# 500,000)")
                acces = result[12]
                if acces == 500000:                 #this line of code will check if you have reach your amount of limitation to borrow in a specified period.
                    print("You have reached your amount to take on loan for the next six month.")
                    log_in()
                elif acces < 500000:            #the request will proceed if you haven't reach the amount limitation.
                    print("Please wait, lets validate your request... ")
                time.sleep(1)
                amount = int(input(" Enter amount you want to borrow: "))
                if amount > 500000:                 #it will check if amount input is greater than your limitation.                  
                    print("you do not have access to this amount. Your limitation is Five Hundred Thousand Naira. Retry!")
                    member_loan()
                elif amount <= 500000:          #it will proceed with the request if you are within your limitation.
                    print("please wait, your request is being process..")
                    querry = "SELECT * from treasures where ID = %s"                #the society treasure account will be call on here.
                    val = (1, )
                    cursor.execute(querry, val)
                    res = cursor.fetchone()
                    newvall = res[1] - amount                       # loan will be deducted from the trasure account via this line of code.
                    time.sleep(1)
                    print(f"You have been successfully granted {amount} of loan from Junaid Cooperative Society. Thank you")
                    qury = "UPDATE treasures SET JCS_Treasure = %s where ID = %s"           #treasure will be update after laon is deducted.
                    val3 = (newvall, 1)
                    cursor.execute(qury, val3)
                    myconn.commit()
                    vall1 = result[12] + amount                                 #loan column will be updated with the amount taken.
                    qu = "UPDATE member SET Loan =%s where Member_id = %s" 
                    val4 = (vall1, Member_id)
                    cursor.execute(qu, val4)
                    myconn.commit()
                    interest = 5                                #interest expected to be added to the loan when paying back.
                    percentage = 100
                    div = amount / percentage * interest
                    refund = amount + div + result[13]                      #amount expected to refund when paying back the loan.
                    querry = "UPDATE member SET Status =%s where Member_id = %s"
                    value = (refund, Member_id)
                    cursor.execute(querry, value)
                    myconn.commit()
    else:
        print("You aren't a registered member of the Association.")
        from Homepage import homepage
        homepage()


#NON MEMBERS WILL HAVE ACCESS TO LOAN HERE
def non_member_loan():
    global User_id
    User_id = input("Enter your user id: ")             # users id will be required here to check if its a registered user.
    value = (User_id, )
    query = "SELECT * from non_member where User_id = %s"
    cursor.execute(query, value)
    result = cursor.fetchone()
    if result:
        access = result[10]         # line of code will check if you have not reach amount limitation to borrow in next six month.
        if access == 300000:
            print("You have reached your amount to take on loan for the next six month.")
            loanee_log_in()
        elif access < 300000:
            print("Please wait, lets validate your request... ")
            time.sleep(1)
        debt = result[11]               # line of code will check your status if you owe money or not
        if debt > 0:
            print("Dear, User, your access to take on loan denied! Kindly clear off your debt!")
            refund_loan()
        elif debt == 0:
            print(f"You want to take loan as {result[1]} {result[2]} {result[3]}")          # if your status is zero you will be allow to borrow.
            time.sleep(1)
            print("Dear user, kindly go through our Loan Application Rules before embarking on it. Thank you!")
            time.sleep(1)           # few rules to have access to take on loan.
            print("""
                        JCS RULES ON LOAN (APPLICABLE TO USER / LOANEE ONLY)
            1. To access our loan page, you must created an account with us via our online app (JCS).
            2. Your user ID shall be your access to our loan page, if you aren't a registered user / loanee kindly do so before attempting the loan page.
            3. As a non - member of this Association, you only have access to take on loan up to Three Hundred Thousand Naira Only (#300,000). 
            4. As a non - member of the Association, the interest of the loan taken shall (15%) of the amount.
            5. A partial amortization is not allowed. We accept a full amortization ONLY.
            6. You have ACCESS to take amount of Five Hundred Thousand (#500,000) on loan in SIX MONTH!
            """)
            time.sleep(1)               # you can proceed with the request if you are a registered users and good with the rules.
            print("""Enter
            1. to proceed with the loan application
            2. to register an account with us
            3. home
            """)
            decision = input(">>> ")
            if decision == "1":
                print("Dear User, you have access to take on loan up to Three Hundred Thousand Naira (# 300,000)")
                amount = int(input(" Enter amount you want to borrow: "))
                if amount > 300000:         # line of code will check if the amount to borrow is not greater than the limitation.
                    print("you do not have access to this amount. Your limitation is Three Hundred Thousand Naira. Retry!")
                    non_member_loan()
                elif amount <= 300000:      # you can proceed with the request if the amount is less or equal to the limitation.
                    print("please wait, your request is being process..")
                    querry = "SELECT * from treasures where ID = %s"
                    val = (1, )
                    cursor.execute(querry, val)
                    res = cursor.fetchone()
                    newvaal = res[1] - amount       # line of code will deduct amount from the society treasure on the table named.
                    time.sleep(1)
                    print(f"You have been successfully granted {amount} of loan from Junaid Cooperative Society. Thank you") # loan taken succesful.
                    qury = "UPDATE treasures SET JCS_Treasure = %s where ID = %s"       # the treasure will be updated after the loan deduction.
                    vaal = (newvaal, 1)
                    cursor.execute(qury, vaal)
                    myconn.commit()
                    vall1 = result[10] + amount         # loan column will be updated with the amount borrowed in total.
                    qu = "UPDATE non_member SET Loan =%s where User_id = %s" 
                    val4 = (vall1, User_id)
                    cursor.execute(qu, val4)
                    myconn.commit()
                    interest = 15
                    percentage = 100
                    div = amount / percentage * interest       # the code shows the interest adds to the loan
                    refund = amount + div + result[11]              # amount borrow plus the interest on it will be added here and update.
                    querry = "UPDATE non_member SET Status =%s where User_id = %s"      # amount expected to refund when paying back the loan.
                    value = (refund, User_id)
                    cursor.execute(querry, value)
                    myconn.commit()
                else:
                    print("You aren't a registered user of the Association.")
            elif decision == "2":
                from registration import reg
                reg()
            elif decision == "3":
                from Homepage import homepage
                homepage()
            else:
                print("Invalid input! Retry!")
                non_member_loan()

#REFUND PAGE FOR BOTH MEMBERS AND NON - MEMBERS
def refund_loan():
    print("This is amortization loan page for Junaid Cooperative Society (JCS).")
    time.sleep(1)
    print("""Enter
    1. to refund as a member
    2. to refund as a non - member 
          """)
    decision = input(">>> ")
    if decision == "1":
        member_refund()                             # member loan refund function.
    elif decision == "2":
        non_member_refund()                         # non member / loanee refund function.
    else:
        print("Invalid, retry.")
        refund_loan()

#def member_refund ALLOWS MEMBER TO REFUND THE LOAN
def member_refund():
    print("This is loan refund page for members")
    global Member_id
    Member_id= input("Enter your Member_id: ")              # member id will be required to verify the member paying back.
    value = (Member_id, )
    query = "SELECT * from member where Member_id = %s"
    cursor.execute(query, value)
    global result
    result = cursor.fetchone()              # member details will be fetched.
    if result:
        print(f"You are making a refund of loan as {result[1]} {result[2]} {result[3]}")        # payer name will be display
        time.sleep(1)
        amount = int(input("Enter amount to refund: "))         # amount to refund
        ref = result[13]
        if amount < ref:        # line of code will check if you are paying in full or partial. if partial, it will be denied.
            print("Partial payment not allow, Pay in full.")
            time.sleep(1)
            member_refund()
        elif amount == ref:         # if refund is in full, you can proceed the payment.
            print("Please wait your refund is being process...")
            time.sleep(2)
            print("Dear member, your loan has been liquidated. Thank you!")         # refund successful.
            bal = int(result[13]-amount)
            val = (bal, Member_id)
            querry_2= "UPDATE member SET Status = %s where Member_id = %s"          # status will be cleared off
            cursor.execute(querry_2, val)
            myconn.commit()
            query3 = "SELECT * from treasures where ID = %s"        # society treasure call upon
            val1 = (1, )
            cursor.execute(query3, val1)
            resul_t = cursor.fetchone()
            if resul_t:
                newvalue3 = resul_t[1] + amount
                newquery3 = "UPDATE treasures SET JCS_Treasure = %s where ID = %s"      # refund payment will be updated on society treasure.
                val4 = (newvalue3, 1)
                cursor.execute(newquery3, val4)
                myconn.commit()
                profit = amount - int(result[12]) #this line of code shows the profit gain from the loan taken from members, and it will be updated on profit, the treasures table.
                val_1 = resul_t[2] + profit
                val_ = (val_1, 1)
                qu_ery = "UPDATE treasures SET profit = %s where ID = %s"
                cursor.execute(qu_ery, val_)
                myconn.commit()
        elif amount > ref:
            print("overpay, cross check your refund.")
            member_refund()


#def non_member_refund ALLOWS NON - MEMBER TO REFUND THE LOAN
def non_member_refund():
    print("This is loan refund page for non - members")
    global User_id
    User_id= input("Enter your User_id: ")      # user id will be required to verify the user paying back.
    value = (User_id, )
    query = "SELECT * from non_member where User_id = %s"
    cursor.execute(query, value)
    global result
    result = cursor.fetchone()          # user details will be fetched.
    if result:
        print(f"You are making a refund of loan as {result[1]} {result[2]} {result[3]}")        # payer name will display.
        time.sleep(1)
        amount = int(input("Enter amount to refund: ")) 
        ref = result[11]
        if amount < ref:            # the code will check if amount input to pay is less than expected amount to refund.
            print("Partial payment not allow, Pay in full.")
            time.sleep(1)
            non_member_refund()
        elif amount == ref:             # if amount input is full payment, request will proceed.
            print("Please wait your refund is being process...")
            time.sleep(2)
            print("Dear user, your loan has been liquidated. Thank you!")       # liquidation successful.
            bal = int(result[11]-amount)        # status cleared.
            val = (bal, User_id)
            querry_2= "UPDATE non_member SET Status = %s where User_id = %s"            # status will be updated
            cursor.execute(querry_2, val)
            myconn.commit()
            query3 = "SELECT * from treasures where ID = %s"
            val1 = (1, )
            cursor.execute(query3, val1)
            resul_t = cursor.fetchone()
            if resul_t:
                newvalue3 = resul_t[1] + amount     # line of code add money refund to the society treasure.
                newquery3 = "UPDATE treasures SET JCS_Treasure = %s where ID = %s"
                val4 = (newvalue3, 1)
                cursor.execute(newquery3, val4)
                myconn.commit()
                profit = amount - int(result[10]) #this line of code shows the profit gain from the loan taken from members, and it will be updated on profit, the treasures table.
                val_1 = resul_t[2] + profit
                vall = (val_1, 1)
                qu_ery = "UPDATE treasures SET profit = %s where ID = %s"
                cursor.execute(qu_ery, vall)
                myconn.commit()
        elif amount > ref:
            print("overpay, cross check your refund.")
            non_member_refund()


#                                          MESSAGE TO THE USER OF THIS PROJECT!
#This is my first python project named "Cooperative Society". This Research / Project filled a lot of gap in project, and i put my best to come
# out with good result. The Theoreitcal aspect / Summary of the project will be uploaded on "READ ME" on GIT HUB. The line of codes in this 
# project is explanatory. But, if you find a gap needed to fill in this project, do not hesitate to take it as a challenge. Research is not
# limit. Do your best, i have done my own challenge in this project, and i might still review the challenge in future. Yes, i might review it
# 'cause there will always be gap to fill in the project, discover it on your own. This project is coded by JUNAID, S. OMOWUMI. Thank you!
