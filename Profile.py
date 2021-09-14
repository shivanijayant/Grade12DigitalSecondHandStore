#!/usr/bin/python3

# catLi to be defined in the main
# Category list for products
ifile = open("category list.txt",'r')
catLi = []
for ln in ifile:
    catLi.append((ln.rstrip()).lower())
ifile.close()

#==========================================================================
# Top of profile page - Imports, username
#==========================================================================
import mysql.connector 
import sys
import tabulate
import random
import os
from datetime import date

cval=50
#==========================================================================
#To print profile page
#==========================================================================
#TESTED - CHECK

#All details of the individual
#Items put up for sale
#Items in cart
#Printing details
def printdet(cursor, uname):
        query = '''Select UserId, Uname, Email, Phno from Users
        where UserId = \''''+str(uname)+"'"
        cursor.execute(query)
        tup = cursor.fetchall()
        print("Profile Details")
        print("-------------")
        print()
        print("User details : ")
        for row in tup:
            print("Username : ", row[1])
            print("User ID : ", row[0])
            print("Email : ", row[2])
            print("Phone Number : ", row[3])
        print()
        print("-------------")

#==========================================================================
# View cart
#==========================================================================
#TESTED - CHECK
def viewCart(cursor, uname):
    # Fetching information from table
    query = '''Select Cart from Users where UName=\''''+uname+"'"
    cursor.execute(query)
    tup = cursor.fetchall()    
    # Display
    print()
    print("----- Cart Items -----".center(cval))    
    prodLi=[]    
    for rec in tup:
        subrec = rec[0]
        cartEle = subrec.split('|@|')
        for item in cartEle:
            prodLi.append(item.split('||'))            
    print(tabulate.tabulate(prodLi, headers = ['Product Name', 'Quantity Ordered']))
    x=input("Press enter to continue")    
    
#==========================================================================
# View items already uploaded
#==========================================================================    
#TESTED - CHECK
def viewItems(cursor, uname, mycon):
    query = '''Select Products from Users where UserID=\''''+uname+"'"
    cursor.execute(query)
    tup = cursor.fetchall()    
    # Display 
    print()
    print("----- Products -----".center(cval))
    print()
    prodLi=[]    
    for rec in tup:
        subrec = rec[0]
        cartEle = subrec.split('|@|')
        for item in cartEle[0:len(cartEle)-1]:
            intermLi = item.split('||')
            prodid = intermLi[0]            
            query = '''Select PName from Products where ProdID={}'''.format(prodid)
            cursor.execute(query)
            tup = cursor.fetchall()
            
            cursor.execute(query)
            if len(cursor.fetchall())!=0:
                pname = tup[0][0]
                prodAppend = [pname,intermLi[1]]
                prodLi.append(prodAppend)
                break
        else:
            print("You've not uploaded products to sell :(")            
    print(tabulate.tabulate(prodLi, headers = ['Product Name', 'Quantity offered']))
    print()
    mycon.commit()
    
#==========================================================================
#Uploading items to sell
#==========================================================================
#TESTED - CHECK
def addProduct(cursor, uname, mycon):
    global catLi    
    # Generating a random product id    
    while True: # As long as a product code as not been found    
        testProdID = random.randint(0, 10**7)
        query = ('''Select ProdID from Products where ProdID='''+str(testProdID))
        cursor.execute(query)
        tup = cursor.fetchall()
        if tup == []:
            break        
    # If there is no other record in the products with this product id
    prodID = testProdID    
    print("Enter: ")    
    # Product Name
    prodName = str(input("Product name: "))    
    #Product Category
    while True:
        catName = input("Category name: ").lower()
        if catName not in catLi:
            print("Please enter a valid product category")
            print()
            ch = input("Would you like to view the possible categories? [y/n]: ")
            if ch.lower() == 'y':
                for category in catLi:
                    print(category)
                    print()
        else:
            break    
    #User ID
    query1 = '''Select UserID from Users where UName=\''''+uname+"'"
    cursor.execute(query1)
    tup = cursor.fetchall()
    userID = tup[0][0]    
    # Product description 
    while True:
        descrip = str(input("Product description (max 200 characters):"))
        if len(descrip) >= 200:
            print("Too long!")
            print()
        else:
            break            
    # Date of upload 
    today = date.today()
    today = today.strftime("%Y-%m-%d")    
    # Price
    price = float(input("Price: "))    
    # Quantity
    qty = int(input("Quantity in stock: "))    
    # Inserting products into Products
    query2 = "Insert into Products values({0},'{1}','{2}','{3}','{4}',{5},'{6}',{7},{8},{9})".format(str(prodID), prodName, catName, userID, descrip, 'NULL', today, str(price), 'NULL', str(qty))    
    cursor.execute(query2)
    # Updating products cart in Users
    query3 = '''Select Products from Users where UName=\''''+uname+"'"
    cursor.execute(query3)
    tup = cursor.fetchall()
    cursor.execute(query3)
    if len(cursor.fetchall())==0:
        products =str(prodID)+"||"+str(qty)+"|@|"
    else:
        products = tup[0][0]+str(prodID)+"||"+str(qty)+"|@|"
    query4 = '''Update Users set Products=\''''+products+"'"+''' where UName=\''''+uname+"'"
    cursor.execute(query4)
    mycon.commit()
    x=input("Item added!!! Press enter to continue")
    os.system("cls")

#==========================================================================
# Log Out
#==========================================================================
#TESTED - CHECK
def logOut():
    print("Thank you for shopping with us! We hope to see you again soon.")
    sys.exit()
    
#==========================================================================
# MAIN
# Only mainProfile has to be called in the main code
# Other function calls have been included in this function
#==========================================================================
UserID=''
def mainProfile(UName):
    mycon = mysql.connector.connect(host='localhost',user='root',passwd='mysql123', database='test')
    cursor = mycon.cursor()    
    uname = UName #Username to be entered as variable here
    os.system("cls")
    print("---- Profile Page ----".center(cval))
    print()
    printdet(cursor, uname)
    x=input("Press enter to continue")
    os.system("cls")
    while True:
        print("----- Menu -----".center(cval))
        print()
        print("""1. View cart
2. Add an item to sell 
3. View all items put up for sale
4. Return to Homepage
5. Log out""")
        print()
        ch = input("Enter menu choice: ")
        while ch not in ['1','2','3','4','5']:
            print("Enter valid menu choice: ")
            continue
        os.system("cls")
        if ch == '1':
            viewCart(cursor, uname)
        elif ch == '2':
            addProduct(cursor, uname, mycon)
        elif ch == '3':
            viewItems(cursor, uname, mycon)
        elif ch == '4':
            import Homepage
            Homepage.menu(mycon,cursor,uname)
        elif ch == '5':
            logOut()
            
