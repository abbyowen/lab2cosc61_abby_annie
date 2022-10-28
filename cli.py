from tempfile import TemporaryFile
from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
import sys
from author_operations import *
from reviewer_operations import *
from ManUser import * 

# INPUTS: 
# TO REGISTER 
# - register|author|<first name>|<last name>|<email>|<affiliation>
# - 

# TO LOGIN
# - login <usertype> <userid>

# TO SUBMIT 
# Delimit author list with a "-" character
# - submit <title> <affiliation> <ICode> - <author2> <author3> <author4> - <filename>


USER_ID = None
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




def read_input(user, input, mycursor, conn):
    
    words = input.strip("\n").split("|")
    # TODO: if command line contains no keywords say I don't understand input
    if words[0] == "register":
       if words[1] == "author":
        id = register_author(mycursor, words)
        if id != "ERROR INPUT":
            user.set_id(id)
            conn.commit()
        if words[1] == "reviewer":
            icodes = []
            if words[4] == "-":
                i = 5
                while words[i] != "-":
                    icodes.append(words[i])
                    i += 1
            id = register_reviewer(mycursor, words, icodes)
            user.set_id(id)
            conn.commit()
        
        return id
    if words[0] == "login":
        if words[1] == "author":
            id = login_author(mycursor, words)
            if id != "ERROR INPUT":
                user.set_id(int(words[2]))
                status(mycursor, user)
            return id
    if words[0] == "submit":
        authors = []
        if words[5] == "-":
            i = 6
            while words[i] != "-":
                authors.append(words[i])
                i += 1
        id = submit_manuscript(user, mycursor, words, authors)
        if id != None:
            conn.commit()
    if words[0] == "status":
        status(mycursor, user)

    if words[0] == "accept":
        man_id = words[1]
        scores = [words[1], words[2], words[3], words[4]]
        decision = 10
        man_review(mycursor, user, scores, man_id, decision)
        
            


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