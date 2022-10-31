# COSC 61, Professor Palmer 
# Authors: Abby Owen, Annie Revers
# author_operations.py - SQL commands for author operations

from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
from ManUser import *


# TODO: File BLOBs for insert manuscript

########### register_author ###########
def register_author(mycursor, words):

    insert_user = "INSERT INTO SysUser (UserType) VALUES (%s)"
    user_type = ("author", )
    
    
    try: 
        mycursor.execute(insert_user, user_type)
        user_id = mycursor.lastrowid

        q1 = "INSERT INTO Author (AuthorId, AuthorFirstName, AuthorLastName, AuthorEmail, AuthorAffiliation) VALUES (%s, %s, %s, %s, %s)"
        val = (user_id, words[2], words[3], words[4], words[5])
        
        mycursor.execute(q1, val)
    
        print(f"Thank you for registering. Your author ID is {user_id}")
        return user_id
    except Error as err:
        print(f"Error registering author: {err}")
        return None


########### login_author ###########
def login_author(mycursor, id):
            
    q = "SELECT * FROM Author WHERE AuthorId = (%s)"
    val = int(id)
    try:
        mycursor.execute(q, (val,))
        res = mycursor.fetchone()
        row = dict(zip(mycursor.column_names, res))
        
        print(f"WELCOME AUTHOR {row['AuthorFirstName']} {row['AuthorLastName']}".format(row))
        return row
        
    except Error as err:
        print(f"Error logging in author, no author found with this ID: {err}")
        return None


########### check_author ###########
def check_author(mycursor, fname, lname, order):
    check_exist_sql = "SELECT EXISTS(SELECT 1 FROM Author WHERE AuthorFirstName = %s AND AuthorLastName = %s)"

    vals = (fname, lname)
    try: 
        mycursor.execute(check_exist_sql, vals)
        res = mycursor.fetchone()
        if res[0] == 0:
            return None
        else:
            get_id_sql = "SELECT AuthorId FROM Author WHERE AuthorFirstName = %s AND AuthorLastName = %s"
            vals = (fname, lname)
            try: 
                mycursor.execute(get_id_sql, vals)
                id = mycursor.fetchone()[0]
                return id
            except Error as err:
                print(f"Error getting co author ID: {err}")
                return None
            
    except Error as err:
        print(f"Error accessing Author database: {err}")


########### submit_response ###########
def submit_response(man_id, mycursor):
    get_status_sql = "SELECT ManStatus, DateUpdated FROM Manuscript WHERE ManuscriptId = %s"
    val = (man_id, )
    try:
        mycursor.execute(get_status_sql, val)
        res = mycursor.fetchone()
        print(f"Recieved manuscript with unique ID: {man_id}")
        print(f"Manuscript {man_id} Status: {res[0]}")
        print(f"Manuscript {man_id} recieved at: {res[1]}")
    except Error as err:
        print(f"Error getting manuscript information: {err}")



########### submit_manuscript ###########
# We must: 
# INSERT INTO Manuscript (Title, ICode) VALUES (%s, %s)
# INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)
# Check if other authors are in the Author database
# If they are not, add them.
# FOR EACH AUTHOR: 
# INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)
def submit_manuscript(user, mycursor, title, icode, authors, filename):
    # Check permissions of user
    if user.get_id() == None:
        print("You do not have the proper permissions for this action. Please log in with you Author ID to submit a manuscript.")
        return None
    
    
    # Insert the manuscript
    insert_man_sql = "INSERT INTO Manuscript (Title, ICodeId) VALUES (%s, %s)"
    vals = (title, icode)
    man_id = None
    try:
        mycursor.execute(insert_man_sql, vals)
        man_id = mycursor.lastrowid

    except Error as err:
        print(f"Error inserting manuscript: {err}")
        return None

    # If the manuscript was inserted, add primary author to author group
    if man_id != None:
        insert_primary_sql = "INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)"
        vals = (man_id, user.get_id(), 1)
        try: 
            mycursor.execute(insert_primary_sql, vals)
        except Error as err:
            print(f"Error inserting primary author: {err}")
            return None
    
    # Check for additional authors
    if len(authors) != 0: 
        for i in range(len(authors)):
            a = authors[i]
            fname, lname = a.split(" ")
            # check if the author is already in the database
            co_id = check_author(mycursor, fname, lname, i)

            # if not, insert the author to the database
            if co_id == None:              
                try:              
                    insert_user = "INSERT INTO SysUser (UserType) VALUES (%s)"
                    u = ("author", )
                    mycursor.execute(insert_user, u)
                    co_id = mycursor.lastrowid

                    insert_co_sql = "INSERT INTO Author (AuthorId, AuthorFirstName, AuthorLastName) VALUES (%s, %s, %s)"
                    vals = (co_id, fname, lname)
                    
                    mycursor.execute(insert_co_sql, vals)
                    
                except Error as err:
                    print(f"Error inserting co-author: {err}")
                    # delete manuscript?
                    return None
            
            # if the author was in the database
            else:
                insert_group = "INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)"
                print(f"Author Group ID: {co_id}")
                vals = (man_id, co_id, i)
                try: 
                    mycursor.execute(insert_group, vals)
                except Error as err:
                    print(f"Error inserting to Author Group: {err}")
    
    submit_response(man_id, mycursor)
    return man_id


########### status ###########
def author_status(mycursor, user):
    try:    
        print("######### MANUSCRIPT STATUSES #########")
        statuses = ["Recieved", "Under Review", "Rejected", "Accepted", "Typesetting", "Ready", "Scheduled", "Published"]
        counts = {}
        for status in statuses:
            get_count = "SELECT COUNT(ManStatus) FROM LeadAuthorManuscripts WHERE AuthorId = %s AND ManStatus = %s"
            vals = (user.get_id(), status)
            mycursor.execute(get_count, vals)
            res = mycursor.fetchone()[0]
            counts[status] = res
            
        for c in counts: 
            print(f"{c}: {counts[c]}")
        # mycursor.execute(status_sql, val)
        # res = mycursor.fetchall()
        
        # output = "Manuscript Statuses \n############## \n Recieved \n ############## \n"
        # for x in res:
            # print(x)
    except Error as err:
        print(f"Error in getting author manuscripts: {err}")

    






    
    

        

    




    

    


