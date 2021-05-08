#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:04:36 2021
-adding function (connecting to database)
-adding function (count all duplicates in table and show them)
-adding function (show all items from tab)
-adding function (print names of columns in table)
-adding function (finding and deliting duplicates)
-adding function (sorting function)
-adding function (deleting data)
-adding function (deleting tab)
-adding function (updating record in tab)
-adding function (limit tab elements for show)
-adding function (limit range of displayed tabs data)
-add menu and better tab show
-add possiblity to creat new tab and import it as classe object
@author: lukas
"""
import mysql.connector
import os
from tabulate import tabulate
import functools
import enquiries
from creat_new_tab import Create_Table 
  

# connecting to database
mydb = mysql.connector.connect(
  host="lukas-ThinkPad-T440",
  user="root",
  password="password",
  database="sql-kurs"
)


# print names of columns in table       
def show_tabl_colum_names(mycursor):
    # first option scheme
    sql = """SELECT COLUMN_NAME
      FROM INFORMATION_SCHEMA.Columns
      WHERE TABLE_SCHEMA = 'sql-kurs' AND TABLE_NAME = 'users';"""
    
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # create one tuple with list of tuples (all with strings)
    myresult = functools.reduce(lambda sub, ele: sub  + ele, myresult)     

    mydb.commit()
    return myresult
    

# show all items from tab
def show_tabl_colum_data(*args):
    len_args = len(args)
    if len_args > 1:
        args[0].execute(args[1])      
    else: 
        args[0].execute("SELECT * FROM users")
        
    myresult = args[0].fetchall() # checking all row   
    # fetch only one row

    tab = show_tabl_colum_names(args[0])
    a, b, c, d = tab
    print(tabulate(myresult, headers=[a, b, c, d]))

        
# count all duplicates in table and show them
def check_if_are_row_duplicates(mycursor):
    sql = """
    SELECT COUNT(*), first_name, last_name, age 
    FROM users
    GROUP BY first_name, last_name, age
    HAVING COUNT(*)>1;print('Duplicate Rows: ')               
    for row in mycursor.fetchall():
    """
    mycursor.execute(sql)    
    
    print('Duplicate Rows: ')               
    for row in mycursor.fetchall(): 
        print(row)
   
    
# finding and deliting duplicates
def del_row_duplicats(mycursor):    
    sql = """
    DROP TABLE IF EXISTS users_temp;
    
    CREATE TABLE users_temp 
    LIKE users;
    
    INSERT INTO users_temp
    SELECT * 
    FROM users 
    GROUP BY username;

    DROP TABLE users;
    
    ALTER TABLE users_temp 
    RENAME TO users;
    """
    mycursor.execute(sql)    
    mydb.commit()
    
    
# sorting ascending or descending    
def sort_funct(mycursor):
    show_tabl_colum_data(mycursor)
    options = ["Order by id [ascending]", "Order by first name [ascending]",
               "Order by last name [ascending]", "Order by age[ascending]",
               "Order by id [descending]", "Order by first name [descending]",
               "Order by last name [descending]", "Order by age[descending]" ]    
     
    choice = enquiries.choose('Choose one of these options: ', options)
    # ascending
    if choice == options[0]:
        sql = "SELECT * FROM users ORDER BY id"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
    elif choice == options[1]:
        sql = "SELECT * FROM users ORDER BY first_name"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
    elif choice == options[2]:
        sql = "SELECT * FROM users ORDER BY last_name"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
    elif choice == options[3]:
        sql = "SELECT * FROM users ORDER BY age"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
    # descending
    elif choice == options[4]:
        sql = "SELECT * FROM users ORDER BY id DESC"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
    elif choice == options[5]:
        sql = "SELECT * FROM users ORDER BY first_name DESC"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
    elif choice == options[6]:
        sql = "SELECT * FROM users ORDER BY last_name DESC"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
    elif choice == options[7]:
        sql = "SELECT * FROM users ORDER BY age DESC"
        show_tabl_colum_data(mycursor, sql)
        any_key_clear()
        

# deleting data support anty injection
def delet_record(mycursor):
    show_tabl_colum_data(mycursor)    
    sql = "DELETE FROM users WHERE age = %s"
    adr = ("66", )
    
    mycursor.execute(sql, adr)   
    mydb.commit()
    
    print(mycursor.rowcount, "record(s) deleted") 


# deleting whole table
def del_table(mycursor):
    sql = "DROP TABLE users"
    mycursor.execute(sql)


# updating record in tab
def updating_record(mycursor):   
    sql = "UPDATE users SET age = %s WHERE id = %s"
    val = ("22", "15")
    
    mycursor.execute(sql, val) 
    # required to make changes
    mydb.commit()
    
    print(mycursor.rowcount, "record(s) affected")    
 
    
# limit tab elements for show
def show_with_limits(mycursor):
    mycursor.execute("SELECT * FROM users LIMIT 5") 
    myresult = mycursor.fetchall()
    
    for x in myresult:
      print(x)     


# limit range of displayed tabs data
def show_with_range(mycursor):
    mycursor.execute("SELECT * FROM users LIMIT 3 OFFSET 2")
    myresult = mycursor.fetchall()
    
    for x in myresult:
      print(x)  
     
      
# print menu      
def menu():
    options = [  
    "List all database.",
    "Create new tab.",
    "Add data to new tab.",
    "Show all items from tab.",
    "Count all duplicates in table and show them.",
    "Finding and deliting duplicates.",
    "Sorting function.",
    "Delete record.",
    "Deleting tab.",
    "Updating record in tab.",
    "Limit tab elements for show.",
    "Limit range of displayed tabs data.",
    "Close programm."]

    # value = int(input("Input value:\n"))
    return options


# clear and continue 
def any_key_clear():    
    input("press any key to continue.")
    os.system('clear')   

# # main function test
# def main():    
#     mycursor = mydb.cursor()    
#     new_tab = Create_Table()


#main function
def main():    
    while True:
        mydb.reconnect()
        mycursor = mydb.cursor()
        new_tab = Create_Table()
        options = menu()
        choice = enquiries.choose('Choose one of these options: ', options)
        if choice == options[0]:
            new_tab.list_all_database(mycursor)
            any_key_clear()
            
        elif choice == options[1]:
            new_tab.create_table(mycursor)
            any_key_clear()
            
        elif choice == options[2]:
            new_tab.insert_data(mycursor, mydb)
            any_key_clear()
            
        elif choice == options[3]:
            show_tabl_colum_data(mycursor)
            any_key_clear()
            
        elif choice == options[4]:
            check_if_are_row_duplicates(mycursor) 
            any_key_clear()
            
        elif choice == options[5]:          
            del_row_duplicats(mycursor) 
            any_key_clear()
            
        elif choice == options[6]:
            sort_funct(mycursor)
            any_key_clear()
            
        elif choice == options[7]:
            delet_record(mycursor)
            any_key_clear()
            
        elif choice == options[8]:
            del_table(mycursor)
            any_key_clear()
            
        elif choice == options[9]:
            updating_record(mycursor)
            any_key_clear()
            
        elif choice == options[10]:
            show_with_limits(mycursor)
            any_key_clear()
            
        elif choice == options[11]:
            show_with_range(mycursor)
            any_key_clear()
            mycursor.close()
            mydb.close()
            
        elif choice == options[12]:
            break
        else:
            print("Incorrect chooise, try again!")
            
       
if __name__ == "__main__":
    main()


