# COSC 61, Professor Palmer 
# Authors: Abby Owen, Annie Revers
# startup.py - add our test data to the database - this will run all of our tables, inserts, triggers, and views
# NOT NECESSARY TO RUN EACH TIME, JUST BEFORE FIRST STARTUP TO ENSURE INFORMATION IS THERE

from tempfile import TemporaryFile
from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
import sys
from shlex import split


###### db_connect ######
# Connect to the database and return the cursor for executing queries and the connection for closing
def db_connect():
    # load database
    dbconfig = read_db_config()
    if dbconfig['password'] == "":  
        dbconfig['password'] = getpass.getpass("database password ? :")
    
    print(dbconfig)
        
    # Connect to the database
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**dbconfig)
 
        if conn.is_connected():
            print('connection established.')
            mycursor = conn.cursor(buffered=True)
            return mycursor, conn
        else:
            print('connection failed.')

    except Error as err:
        print('connection failed somehow')
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Unexpected error")
            print(err)
            sys.exit(1)

###### db_close ######
# Close the db connection given a connection and a cursor
def db_close(conn, mycursor):
    print("All done - closing up.")
    mycursor.close()
    conn.cmd_reset_connection()
    conn.close()
    print("DONE")

###### create_tables #######
# Create the tables from tables.sql
def create_tables(mycursor):
    try:
         # run the tables.sql files, which drops and recreates all of our tables
        f = open("tables.sql", "r")
        query = "".join(f.readlines())
        # go through each statement (delimited by a ; character)
        print("creating tables")
        for s in query.split(";"):
            if len(s) > 0:
                mycursor.execute(s + ";")
        print("done creating tables")
    except Error as err:
        print(f"Error creating tables: {err}")

###### create_triggers #######
# Create triggers from triggers.sql
def create_triggers(mycursor):  
    try:
        print("creating triggers")
        f = open("triggers.sql", "r")
        query = "".join(f.readlines())
        # go through each statement (delimited by a ; character)
        for s in query.split(";"):
            if len(s) > 0:
                mycursor.execute(s + ";", multi=True)
        print("done creatng triggers")
    except Error as err:
        print(f"Error creating triggers: {err}")

    
###### create_data #######
# Insert data from insert.sql
def insert_data(mycursor):
    try:
        print("inserting data")
        f = open("insert.sql", "r")
        query = "".join(f.readlines())
        # go through each statement (delimited by a ; character)
        for s in query.split(";"):
            if len(s) > 0:
                mycursor.execute(s + ";")
        print("done inserting data")
    except Error as err:
        print(f"Error inserting data: {err}")

###### create_views #######
# Create views from views.sql
def create_views(mycursor):
    try:
        print("creating views")
        f = open("views.sql", "r")
        query = "".join(f.readlines())
        # go through each statement (delimited by a ; character)
        for s in query.split(";"):
            if len(s) > 0:
                mycursor.execute(s + ";", multi=True)
        print("done creating views")
    except Error as err:
        print(f"Error creating views data: {err}")

###### db_close ######
# Close the db connection given a connection and a cursor
def db_close(conn, mycursor):
    print("All done - closing up.")
    mycursor.close()
    conn.cmd_reset_connection()
    conn.close()
    print("DONE")


####### start ######
# Main function to create all tables and triggers
def start():

    mycursor, conn = db_connect()
    create_tables(mycursor)
    conn.commit()
    insert_data(mycursor)
    conn.commit()
    create_triggers(mycursor)
    conn.commit()
    create_views(mycursor)
    conn.commit()
    
    print("goodbye!") 

    db_close(conn, mycursor)

    
   
if __name__ == '__main__':
    start()
