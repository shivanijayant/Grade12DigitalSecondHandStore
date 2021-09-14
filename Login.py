import mysql.connector
import os
import getpass
#import other files

connection=mysql.connector.connect(host='localhost',user='shivani', passwd='shivani', database='Test2')
cursor=connection.cursor()
def sign_up():
    a=True
    while a:
        UserID=input("User Name: ")
        cursor.execute('select UserID from users')
        uid=cursor.fetchall()
        for x in uid:
            if UserID in x:
                print('User ID already exists. Enter a different User ID')
                break
        else:
            a=False
    UName=input("Display Name: ")
    print("Password: ", end='')
    Pwd=getpass.getpass()
    Email=''
    while True:
        Email=input("Email ID: ")
        if Email.count('@')==0 or Email.count('.')==0:
            print("Invalid Email")
            continue
        else:
            break
    Phno=0
    while True:
        Phno=int(input("Contact Number: "))
        if len(str(Phno))!=10:
            print("Invalid contact number")
            continue
        else:
            break   
    Address=input("Address: ")
    det=(UserID,UName,Pwd,Email,Phno,Address,'','')
    cursor.execute("insert into users values('{}','{}','{}','{}',{},'{}','{}','{}')".format(UserID,UName,Pwd,Email,Phno,'',Address,''))
    connection.commit()
    os.system("cls")
    import Homepage
    Homepage.menu(connection,cursor,UserID)

UName=''
def login():
    login=1
    while login:
        UName=input("User Name: ")
        print("Password: ", end='')
        Pwd=getpass.getpass()
        cursor.execute('select UserID,UName,Pwd from users')
        tup=cursor.fetchall()
        for rec in tup:
            if (rec[0]==UName and rec[2]==Pwd):
                login=0
                break
            else:
                continue
        if login==1:
            print("Incorrect User Name or Password")
            x=input("Press enter to continue")
            os.system("cls")
    if login==0:
        connection.commit()
        print("Logged in")
        x=input("Press enter to continue")
        os.system("cls")
        import Homepage
        Homepage.menu(connection,cursor,rec[0])

#Main
print("-----Re-Store-----".center(50))
print()
ch=int(input("1. Sign up \n2. Login \nEnter your choice: "))
if ch==1:
    os.system("cls")
    sign_up()
if ch==2:
    os.system("cls")
    login()
