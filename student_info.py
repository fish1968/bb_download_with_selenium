from getpass import getpass


S_ID = "" # Your Student ID
password = "" 

if S_ID == "":
    S_ID = input("Input your student ID:")
if password == "":
    password = getpass("Input your password:")