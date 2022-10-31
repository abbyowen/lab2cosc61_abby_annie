# COSC 61, Professor Palmer 
# Authors: Abby Owen, Annie Revers
# cli.py - the main command line interface for our manuscript system

from tempfile import TemporaryFile
from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
import sys
from author_operations import *
from reviewer_operations import *
from editor_operations import * 
from ManUser import * 
from shlex import split

# INPUTS: 
# TO REGISTER 
# - register author <first name> <last name> <email> <affiliation>
# - register reviewer <first name> <last name> <ICode1> <ICode2> <ICode3>
# - register editor <first name> <last name>

# TO LOGIN (Author, Reviewer, Editor)
# - login <userid>

# TO SUBMIT A MANUSCRIPT (Author)
# - submit <title> <Affiliation> <ICode> <author2> <author3> <author4> <filename>


###### on_startup ######
# Displays message when the program is started
def on_startup():
    print("HELLO, please login or register to access Manuscript system.")


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

###### get_user_type ######
# Get the type of the user based off of the universal system ID
def get_user_type(mycursor, id):
    get_sql = "SELECT UserType FROM SysUser WHERE UniversalId = %s"
    vals = (id, )

    try: 
        mycursor.execute(get_sql, vals)
        user_type = mycursor.fetchone()
        if user_type == None:
            return None
        return user_type[0]
    except Error as err:
        print(f"Error fetching user: {err}")
        return None

###### read_input ######
# Parses the user input for calling according author, editor, reviewer functions 
def read_input(user, input, mycursor, conn):

    # split input by space
    words = split(input)

    # register user
    if words[0] == "register": 
        # register author <first name> <last name> <email> <affiliation>
        if words[1] == "author" and len(words) == 6:
            id = register_author(mycursor, words)
            if id:
                user.set_id(id)
                user.set_role("author")
                conn.commit()
        # register reviewer <first name> <last name> <ICode1> <ICode2> <ICode3>
        elif words[1] == "reviewer" and (len(words) >= 5 and len(words) <= 7):
            first = words[2]
            last = words[3]
            icodes = []
            i = 4
            while i < len(words):
                icodes.append(words[i])
                i += 1
            id = register_reviewer(mycursor, first, last, icodes)
            if id: 
                user.set_id(id)
                user.set_role("reviewer")
                conn.commit()
        # register editor <first name> <last name>
        elif words[1] == "editor" and len(words) == 4:
            id = register_editor(mycursor, words[2], words[3])
            if id: 
                user.set_id(id)
                user.set_role("editor")
                conn.commit()
        else:
            print("Error registering user: invalid type or number of arugments")
    
    # login user
    elif words[0] == "login":
        # check number of arguments
        if len(words) != 2:
            print("Invalid number of arguments. Please login by typing \"login <userid>\"")
        else:
            id = words[1]
            t = get_user_type(mycursor, id)
            if t == "author":
                res = login_author(mycursor, id)
                if res != None:
                    user.set_id(id)
                    user.set_role("author")
            elif t == "reviewer":
                res = reviewer_login(mycursor, id)
                if res != None:
                    user.set_id(id)
                    user.set_role("reviewer")
            elif t == "editor":
                res = login_editor(mycursor, words[1])
                if res != None:
                    user.set_id(id)
                    user.set_role("editor")
            elif t == None:
                print("No user with that ID. Please try again.")
    
    elif words[0] == "submit":
        if user.get_role() == "author" and (4 <= len(words) <= 8):
            filename = words[-1]
            title = words[1]
            icode = words[3]
            i = 5
            authors = []
            while i < len(words) - 1:
                authors.append(words[i])
                i += 1
            id = submit_manuscript(user, mycursor, title, icode, authors, filename)
            if id != None:
                conn.commit()
        else:
            print("You are not an author or provided incorrect number of arguments.")
    
    elif words[0] == "status":
        # check number of arguments
        if len(words) == 1:
            # check role
            if user.get_role() == "author":
                author_status(mycursor, user)
            elif user.get_role() == "editor":
                editor_status(mycursor)
        else:
            print("Invalid number of arguments. Please type \"status\" to check your status.")

    elif words[0] == "accept":
        # check role and number of arguments
        if user.get_role() == "reviewer" and len(words) == 6:
            # role is reviewer
            man_id = words[1]
            scores = [words[1], words[2], words[3], words[4]]
            decision = 10
            man_review(mycursor, user, scores, man_id, decision)
            conn.commit()
        elif user.get_role() == "editor" and len(words) == 2:
            # role is editor
            editor_accept(mycursor, words[1])
            conn.commit()
        else:
            print("Incorrect role or number of arguments.")

    elif words[0] == "reject":
        #  check role and number of arguments
        if user.get_role() == "reviewer" and len(words) == 6:
            # role is reviewer
            man_id = words[1]
            scores = [words[1], words[2], words[3], words[4]]
            decision = 0
            man_review(mycursor, user, scores, man_id, decision)
            conn.commit()
        elif user.get_role() == "editor" and len(words) == 2:
            # role is editor
            editor_reject(mycursor, words[1])
            conn.commit()
    
    elif words[0] == "resign":
        # check role
        if user.get_role() == "reviewer" and len(words) == 1:
            resign(mycursor, user) 
            conn.commit()
        else:
            print("You do not have the proper permissions to resign or provided incorrect number of arguments.")
                
    elif words[0] == "assign":
        # check role and number of arguments
        if user.get_role() == "editor" and len(words) == 3:
            rev_id = words[1]
            man_id = words[2]
            assign(mycursor, rev_id, man_id)
        else:
            print("You do not have the proper permissions to assign a manuscript or entered incorrect number of arguments.")
    
    elif words[0] == "publish":
        # check role and number of arguments
        if user.get_role() == "editor" and len(words) == 2:
            publish(mycursor, words[1])
            conn.commit()
        else:
            print("You do not have the proper permissions to publish a manuscript or entered incorrect number of arguments.")

    elif words[0] == "schedule":
        # check role and number of arguments
        if user.get_role() == "editor" and len(words) == 3:
            man_id = words[1]
            issue_info = words[2]
            i = issue_info.split("-")
            if len(i != 2):
                print("Incorrect issue info. Please input the issue in the form <publication year>-<publication period>")
            else:
                pub_year = i[0]
                pub_period = i[1]
                schedule(mycursor, man_id, pub_period, pub_year)
                conn.commit()
        else:
            print("You do not have the proper permissions to schedule a manuscript or entered incorrect number of arguments.")
    
    elif words[0] == "reset":
        # check role and number of arguments
        if user.get_role() == "editor" and len(words) == 1:
            reset(mycursor) 
            conn.commit()

            sql_check_drop = "SELECT * FROM Reviewer"
            mycursor.execute(sql_check_drop)
            res = mycursor.fetchall()
            for x in res:
                print(x)
            # TEST IF THE TRIGGERS RERAN
            test_insert = "INSERT INTO Manuscript (Title, ICodeId) VALUES (\"mooch tails\", 1)"
            try:
                mycursor.execute(test_insert)
                res = mycursor.lastrowid
                print(res)
                conn.commit()
            except Error as err:
                print(err)
        else:
            print("You do not have the proper permissions to reset the database or entered incorrect number of arguments.")
        
 

    else:
        print("UNKNOWN INPUT.")
            
###### run ######   
# Main functionality, gets stdin and calls read_input to parse input    
def run():
    # Display start message
    on_startup()
    user = ManUser()
    mycursor, conn = db_connect()

    for line in sys.stdin:
        if 'logout' == line.rstrip():
            break
        else:
            read_input(user, line, mycursor, conn)
    
    
    print("goodbye!") 

    db_close(conn, mycursor)
        
   
if __name__ == '__main__':
    run()