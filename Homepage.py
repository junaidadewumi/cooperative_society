import time
import sys

#This is homepage for the cooperative  society. user can select the operation he/she want to perform.
def homepage():
    print("Welcome to Junaid Cooperative Society (JCS)!!!")
    time.sleep(1)
    print("""
    1. Registration of an account for (Member and Non - Member / Loanee)
    2. Log in (Member and Non - Member / Loanee)
    3. Exit the system (Exit)
    """)
    time.sleep(2)
    decision = input(">>> ")
    if decision == "1":
        from registration import reg
        reg()                                           #this function will take you to registration page
    elif decision == "2":
        from loginpage import log
        log()                                           #this function will take you to log in page
    elif decision == "3":
        sys.exit()                                      #this function will exit the page
    else:
        print("Errorneous! Input Again")
        homepage()
homepage()