import tabulate
import os
import sys
#=========================================
# To remove a product from the cart
#=========================================
def RemoveProd(cursor, uname,connection):
    os.system("cls")
    print("-----Remove from Cart-----".center(50))
    print()
    Display(cursor, uname,connection)
    print("Enter Product ID of item you wish to remove from cart: ")
    ID=input("Or enter 'Exit' to return to homepage: ")
    if ID.lower()!='exit':
        Qty=input("Enter Quantity of item you wish to remove from cart: ")
        cursor.execute("Select Cart from users where UserID = '{}'".format(uname))
        cart = cursor.fetchall()[0][0]
        cartEle = cart.split('|@|')
        prodLi=[]
        for item in cartEle:
            prodLi.append(item.split('||'))
        new_Cart=''
        for i in prodLi[0:len(prodLi)-1]:
            if i[0]!=ID:
                new_Cart=new_Cart+i[0]+'||'+i[1]+'|@|'
            if i[0]==ID:
                if Qty>i[1]:
                    print("You do not have that many in your cart")
                    x=input("Press enter to continue")
                    RemoveProd(cursor, uname,connection)
                elif Qty<i[1]:
                    new_Cart=new_Cart+i[0]+'||'+str(int(i[1])-int(Qty))+'|@|'
        cursor.execute("Update users set cart = '{}' where userID = '{}'".format(new_Cart,uname))
        connection.commit()
    main(cursor, uname,connection)

#=========================================
# To display products in the cart
#=========================================    
def Display(cursor, uname,connection):
    os.system("cls")
    print("-----Checkout-----".center(50))
    print()
# Fetching information from table
    query = '''Select Cart from Users where UName=\''''+uname+"'"
    cursor.execute(query)
    tup = cursor.fetchall()         
    prodLi=[]    
    for rec in tup:
        subrec = rec[0]
        cartEle = subrec.split('|@|')
        for item in cartEle:
            prodLi.append(item.split('||'))
    IDs,Qtys,Prices,Names,TotalPrices=[],[],[],[],[]
    for i in prodLi[0:len(prodLi)-1]:
        IDs.append(i[0])
        cursor.execute("select PName from Products where ProdID = '{}'".format(i[0]))
        Names.append(cursor.fetchall()[0][0])
        Qtys.append(i[1])
        cursor.execute("select Price from Products where ProdID = {}".format(i[0]))
        price=cursor.fetchall()[0][0]
        Prices.append(price)
        TotalPrices.append(int(i[1])*int(price))        
    L=[]
    for i in range(len(IDs)):
        L.append([IDs[i],Qtys[i],Prices[i],TotalPrices[i]])
    print()
    print("----- Re-Store -----".center(50)) 
    print(tabulate.tabulate(L, headers = ['Product Id', 'Product Name', 'Quantity Ordered','Price per unit','Total Price']))
    total=0
    for i in L:
        total+=int(i[4])
    print("Total Bill Amount:",total)
    print()

#=========================================
# Main Checkout Page
#=========================================    
def main(cursor, uname,connection):
    Display(cursor, uname,connection)
    ans=input("Confirm the bill?[y/n]").lower()
    while ans not in 'yn':
        ans=input('''
Incorrect input. 
Confirm the bill?[y/n]''').lower()
    if ans=='y':
# Clear Cart
        cursor.execute("Update Users set Cart = ''")
        for i in range(len(IDs)):
            cursor.execute("Select Qty from Products where ProdID = {}".format(IDs[i]))
            qty=int(cursor.fetchall()[0][0])-int(Qtys[i])
            if qty==0:
# Remove Item if qty becomes 0
                cursor.execute("Delete from Products where ProdID = {}".format(IDs[i]))
            else:
# Reduce qty 
                cursor.execute("Update Products set Qty = {}".format(qty))
            connection.commit()
        print("Transaction complete!!!")
        x=input("Press enter to continue")
    os.system("cls")
    print("-----Menu-----".center(50))
    print()
    while ans not in ['1','2','3']:
# Menu Options
        ans=input('''
ENTER:
1 to return to Homepage
2 to remove item from cart
3 to log out
Enter your choice: ''')
    if ans=='1':
        import Homepage
        Homepage.menu(connection,cursor,uname)
    elif ans=='2':
        RemoveProd(cursor, uname,connection)
    elif ans=='3':
        print("Thank you for shopping with us! We hope to see you again soon.")
        sys.exit()
