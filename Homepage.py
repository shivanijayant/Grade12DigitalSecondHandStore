#required modules imported
import mysql.connector
import sys
import tabulate
import os

#main menu
def menu(connection,cursor,UserID):
    os.system("cls")
    print("-----Home Page-----".center(50))
    print()
    ch=1
    while ch in(1,2,3):
        ch=int(input('''1. Products available.
2. Profile.
3. Checkout.
Enter appropriate number:'''))
        while ch not in(1,2,3):
            print('Invalid input.')
            ch=int(input('''1. Products available.
2. Profile.
3. Checkout.
Enter appropriate number:'''))
        os.system("cls")
        if ch==1:
            productpage(connection,cursor,UserID)
        elif ch==2:
            import Profile
            Profile.mainProfile(UserID)
        elif ch==3:
            import Checkout
            Checkout.main(cursor,UserID,connection)

#display all available products and details    
def productpage(connection,cursor,UserID):
#gives basic details of all products
    print("-----Products-----".center(50))
    print()
    query='''Select ProdID,PName,Category from Products'''
    cursor.execute(query)
    result=cursor.fetchall()
    c=1
    for row in result:
        print("Product",c,"-")
        c+=1
        print("Product ID:",row[0])
        print("Product Name:",row[1])
        print("Category:",row[2])
        print()
    print()
#to obtain more details on a specific product
    ProdID=int(input("Enter the Product ID to get more information:"))
    os.system("cls")
    print("-----Product Details-----".center(50))
    print()
    query1='''Select * from Products where ProdID={}'''.format(ProdID)
    cursor.execute(query1)
    result=cursor.fetchall()
    for row in result:
        print("Product ID:",row[0])
        print("Product Name:",row[1])
        print("Category:",row[2])
        print("User ID:",row[3])
        print("Description:",row[4])
        print("Date of Purchase:",row[5])
        print("Date of Uploading:",row[6])
        print("Price:",row[7])
        print("Picture:",row[8])
        print("Quantity in stock:",row[9])
        print()
    print()
    x=input("Press enter to continue")
    print()
    check=0
    check=int(input('''1. Add this item to the cart.
2. Search for more items.
3. Return to homepage.
Enter appropriate number:'''))
    while check not in(1,2,3):
            print('Invalid input.')
            ch=int(input('''1. Add this item to the cart.
2. Search for more items.
3. Return to homepage.
Enter appropriate number:'''))
    os.system("cls")
#add to cart
    if check==1:
        print("-----Add to Cart-----".center(50))
        print()
        qty=int(input("Enter the quantity of the product you wish to purchase:"))
        cursor.execute('''Select Qty from Products where ProdID={}'''.format(ProdID))
        qty1=cursor.fetchall()
#check condition
        while qty>qty1[0][0]:
            qty=int(input("Quantity not available. Please select fewer items: "))
        query2="Select Cart from Users where UserID='{}'".format(UserID)
        cursor.execute(query2)
        cart_val=cursor.fetchall()
        s1=str(ProdID)+'||'+str(qty)+'|@|'
        s2=cart_val[0][0]+s1
        query="Update Users set Cart='{}'".format(s2)
        cursor.execute(query)
        connection.commit()
        menu(connection,cursor,UserID)
    elif check==2:
#return to product page 
        productpage(connection,cursor,UserID)
    elif check==3:
#return to main menu
        menu(connection,cursor,UserID)
        while qty>qty1[0][0]:
            qty=int(input("Quantity not available. Please select fewer items: "))
        query2='''Select Cart from Users where UserID="{}"'''.format(UserID)
        cursor.execute(query2)
        cart_val=cursor.fetchall()
        s1=str(ProdID)+'||'+str(qty)+'|@|'
        query="Update Users set Cart=Cart+'{}'".format(s1)
        cursor.execute(query)

connection=mysql.connector.connect(host='localhost',user='root', passwd='mysql123', database='Test')
cursor=connection.cursor()

UserID=''
