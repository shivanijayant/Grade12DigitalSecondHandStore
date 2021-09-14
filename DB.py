import mysql.connector
from mysql.connector import Error

#Create user table
def createusers():
    query='''Create table Users
(UserID varchar(20) Primary Key,
UName varchar(20),
Pwd varchar(20),
Email varchar(50),
Phno bigint,
Products text(65000),
Address varchar(100),
Cart text(65000))
'''
    cursor.execute(query)
    print("Created table Users.")

#Create products table
def createprod():
    query='''Create table Products
(ProdID integer Primary Key,
PName varchar(30),
Category varchar(20),
UserID varchar(20),
Description varchar(200),
DOP year,
DOU date,
Price Decimal(10,3),
Picture varchar(40),
Qty integer)
'''
    cursor.execute(query)
    print("Created table Products.")

#Create database      
try:
    connection=mysql.connector.connect(host='localhost',user='shivani', passwd='shivani', database='mysql')
    query='''Create database Test2'''
    cursor=connection.cursor()
    cursor.execute(query)
    print("Database Test2 created")
except mysql.connector.Error as error:
    print("Failed to create table:{}".format(error))
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

#Basic inputs into db (hard-coding)
x=1
while x!=5:
    x=int(input('''1. Create table Users.
2. Create table Products.
3. Exit.
Enter the appropriate number: '''))
    try:
        connection=mysql.connector.connect(host='localhost',user='shivani', passwd='shivani', database='Test2')
        cursor=connection.cursor()
        print("Using database Test2")
        print()
        if x==1: 
            createusers()
        elif x==2:
            createprod()
        query='''Insert into Products
Values(11,'Harry Potter Book Series','Books','2',
'The full Harry Potter book series in hardcovers.',
'2017','2020-03-16',3000,"11",2)'''
        cursor.execute(query)
        query='''Insert into Users
Values('2','Madhu','ABC123','madhu56@gmail.com',76234007956,
'2prod','56,5th Cross,Koramangala,Bangalore','2cart')'''
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as error:
        print("Failed to create/insert into table: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")
    print()
    if x==3:
        break
    
