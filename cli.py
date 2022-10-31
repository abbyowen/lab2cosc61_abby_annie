from tempfile import TemporaryFile
from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
import sys
from author_operations import *
from reviewer_operations import *
from ManUser import * 
from shlex import split

# INPUTS: 
# TO REGISTER 
# - register author <first name> <last name> <email> <affiliation>
# - register reviewer <first name> <last name> <ICode1> <ICode2> <ICode3>

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


def get_user_type(mycursor, id):
    get_sql = "SELECT UserType FROM SysUser WHERE UniversalId = %s"
    vals = (id, )

    try: 
        mycursor.execute(get_sql, vals)
        user_type = mycursor.fetchone()
        return user_type[0]
    except Error as err:
        print(f"Error fetching user: {err}")
        return None


def read_input(user, input, mycursor, conn):
    
    words = split(input)
    # TODO: checks for if user is in the database
    # TODO: page numbers?
    if words[0] == "register":
        if words[1] == "author":
            id = register_author(mycursor, words)
            if id != "ERROR INPUT":
                user.set_id(id)
                user.set_role("author")
                conn.commit()
        elif words[1] == "reviewer":
            if len(words) < 5 or len(words) > 7:
                print("Error registering user: not enough ICodes supplied. Must be at least one and up to 3")
            first = words[2]
            last = words[3]
            icodes = []
            i = 4
            while i < len(words):
                icodes.append(words[i])
                i += 1
            id = register_reviewer(mycursor, first, last, icodes)
            user.set_id(id)
            user.set_role("reviewer")
            conn.commit()
            
        return id
    
    elif words[0] == "login":
        if len(words) != 2:
            print("Please login by typing \"login <userid>\"")
        else:
            id = words[1]
            t = get_user_type(mycursor, id)
            if t == "author":
                login_author(mycursor, id)
                user.set_id(id)
                user.set_role("author")
            elif t == "reviewer":
                reviewer_login(mycursor, id)
                user.set_id(id)
                user.set_role("reviewer")
            elif t == None:
                print("No user with that ID. Please try again.")
    
    elif words[0] == "submit":
        if user.get_role() != "author":
            print("You do not have the proper permissions to submit a manuscript. Please log in using a valid author ID and try again.")
        else:
            filename = words[-1]
            title = words[1]
            icode = words[3]
            pages = words[4]
            i = 5
            authors = []
            while i < len(words) - 1:
                authors.append(words[i])
                i += 1
            id = submit_manuscript(user, mycursor, title, icode, pages, authors, filename)
            if id != None:
                conn.commit()
    
    elif words[0] == "status" and user.get_role() == "author":
        author_status(mycursor, user)

    elif words[0] == "accept" and user.get_role() == "reviewer":
        man_id = words[1]
        scores = [words[1], words[2], words[3], words[4]]
        decision = 10
        man_review(mycursor, user, scores, man_id, decision)
    
    elif words[0] == "reject" and user.get_role() == "reviewer":
        man_id = words[1]
        scores = [words[1], words[2], words[3], words[4]]
        decision = 0
        man_review(mycursor, user, scores, man_id, decision)
    
    elif words[0] == "resign":
        if user.get_role() != "reviewer":
            "You do not have the proper permissions to resign. Please log in using your reviewer ID and try again."
        else:
            resign(mycursor, user) 
    else:
        print("UNKNOWN INPUT.")
    

        

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