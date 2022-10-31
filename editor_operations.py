from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
from ManUser import *

# TODO: File BLOBs for insert manuscript

########### register_author ###########
def register_editor(mycursor, firstname, lastname):

    print(firstname)
    print(lastname)

    insert_user = "INSERT INTO SysUser (UserType) VALUES (%s)"
    user_type = ("editor", )
    mycursor.execute(insert_user, user_type)
    id = mycursor.lastrowid
    print("ID ", id)

    q1 = "INSERT INTO Editor (EditorFirstName, EditorLastName, EditorId) VALUES (%s, %s, %s)"
    val = (firstname, lastname, id)
    try: 
        mycursor.execute(q1, val)
        print(f"Thank you for registering. Your editor ID is {id}.")
        return id
    except Error as err:
        print(err.msg)
        print(f"Error registering editor: {err}")

########## login_author ###########
def login_editor(mycursor, id): 
    q = "SELECT * FROM Editor WHERE EditorId = (%s)"
    val = int(id)
    try:
        mycursor.execute(q, (val,))
        row = dict(zip(mycursor.column_names, mycursor.fetchone()))
        print(f"WELCOME {row['EditorFirstName']} {row['EditorLastName']}".format(row))
        
        return row
    except Error as err:
        print(err)
        return "ERROR INPUT"

########### status ###########
def editor_status(mycursor, user):
    if user.get_id() == None:
        print("You do not have the proper permissions for this action. Please log in with you Editor ID to submit a manuscript.")
    else: 
        # status_sql = "SELECT ManuscriptId, Title, DateUpdated, ManStatus FROM LeadAuthorManuscripts WHERE AuthorId = %s"
        # val = (user.get_id(), )
        print("######### MANUSCRIPT STATUSES #########")
        try:    
            get_count = "SELECT * FROM AnyAuthorManuscripts ORDER BY ManStatus ASC, ManuscriptId ASC"
            mycursor.execute(get_count)
            res = mycursor.fetchall()
            for manuscript in res: 
                print(manuscript)
        except Error as err:
            print(f"Error in getting author manuscripts: {err}")
    
########### assign ###########
def assign(mycursor, user, reviewer_id, manuscript_id):
    if user.get_id() == None:
        print("You do not have the proper permissions for this action. Please log in with you Editor ID to submit a manuscript.")
    else: 
        try:    
            q1 = "INSERT INTO Review (ReviewerId, ManuscriptId) VALUES (%s, %s)"
            vals = (int(reviewer_id), int(manuscript_id))
            mycursor.execute(q1, vals)
            # print last review inserted
            my_select = "SELECT * FROM Review WHERE ReviewerId = %s AND ManuscriptId = %s"
            vals3 = (reviewer_id, manuscript_id)
            mycursor.execute(my_select, vals3)
            res = mycursor.fetchone()
            print(res)
            # 60
            # 11

            q2 = "UPDATE Manuscript SET ManStatus = 'under review' WHERE ManuscriptId = %s"
            vals2 = (manuscript_id, )
            mycursor.execute(q2, vals2)
            # print updated manuscript
            my_select2 = "SELECT * FROM Manuscript WHERE ManuscriptId = (%s)"
            vals4 = (manuscript_id,)
            mycursor.execute(my_select2, vals4)
            res2 = mycursor.fetchone()
            print(res2)
            
        except Error as err:
            print(f"Error in getting author manuscripts: {err}")


# ########### check_author ###########
# def check_author(mycursor, fname, lname, order):
#     check_exist_sql = "SELECT EXISTS(SELECT 1 FROM Author WHERE AuthorFirstName = %s AND AuthorLastName = %s)"

#     vals = (fname, lname)
#     try: 
#         mycursor.execute(check_exist_sql, vals)
#         res = mycursor.fetchone()
#         if res[0] == 0:
#             return None
#         else:
#             get_id_sql = "SELECT AuthorId FROM Author WHERE AuthorFirstName = %s AND AuthorLastName = %s"
#             vals = (fname, lname)
#             try: 
#                 mycursor.execute(get_id_sql, vals)
#                 id = mycursor.fetchone()[0]
#                 return id
#             except Error as err:
#                 print(f"Error getting co author ID: {err}")
#                 return None
            
#     except Error as err:
#         print(f"Error accessing Author database: {err}")


# ########### submit_response ###########
# def submit_response(man_id, mycursor):
#     get_status_sql = "SELECT ManStatus, DateUpdated FROM Manuscript WHERE ManuscriptId = %s"
#     val = (man_id, )
#     try:
#         mycursor.execute(get_status_sql, val)
#         res = mycursor.fetchone()
#         print(f"Recieved manuscript with unique ID: {man_id}")
#         print(f"Manuscript {man_id} Status: {res[0]}")
#         print(f"Manuscript {man_id} recieved at: {res[1]}")
#     except Error as err:
#         print(f"Error getting manuscript information: {err}")



# ########### submit_manuscript ###########
# # We must: 
# # INSERT INTO Manuscript (Title, ICode) VALUES (%s, %s)
# # INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)
# # Check if other authors are in the Author database
# # If they are not, add them.
# # FOR EACH AUTHOR: 
# # INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)
# def submit_manuscript(user, mycursor, words, authors):
#     # Check permissions of user
#     if user.get_id() == None:
#         print("You do not have the proper permissions for this action. Please log in with you Author ID to submit a manuscript.")
#         return None
    
    
#     # Insert the manuscript
#     insert_man_sql = "INSERT INTO Manuscript (Title, ICodeId, PageCount) VALUES (%s, %s, %s)"
#     vals = (words[1], words[3], words[4])
#     man_id = None
#     try:
#         mycursor.execute(insert_man_sql, vals)
#         man_id = mycursor.lastrowid

#     except Error as err:
#         print(f"Error inserting manuscript: {err}")
#         return None

#     # If the manuscript was inserted, add primary author to author group
#     if man_id != None:
#         insert_primary_sql = "INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)"
#         vals = (man_id, user.get_id(), 1)
#         try: 
#             mycursor.execute(insert_primary_sql, vals)
#         except Error as err:
#             print(f"Error inserting primary author: {err}")
#             return None
    
#     # Check for additional authors
#     if len(authors) != 0: 
#         for i in range(len(authors)):
#             a = authors[i]
#             fname, lname = a.split(" ")
#             # check if the author is already in the database
#             co_id = check_author(mycursor, fname, lname, i)

#             # if not, insert the author to the database
#             if co_id == None:
#                 insert_co_sql = "INSERT INTO Author (AuthorFirstName, AuthorLastName) VALUES (%s, %s)"
#                 vals = (fname, lname)
                
#                 try: 
#                     mycursor.execute(insert_co_sql, vals)
#                     co_id = mycursor.lastrowid
#                 except Error as err:
#                     print(f"Error inserting co-author: {err}")
#                     # delete manuscript?
#                     return None
            
#             # if the author was in the database
#             else:
#                 insert_group = "INSERT INTO AuthorGroup (ManuscriptId, AuthorId, OrderNum) VALUES (%s, %s, %s)"
#                 print(f"Author Group ID: {co_id}")
#                 vals = (man_id, co_id, i)
#                 try: 
#                     mycursor.execute(insert_group, vals)
#                 except Error as err:
#                     print(f"Error inserting to Author Group: {err}")
    
#     submit_response(man_id, mycursor)
#     return man_id



    






    
    

        

    




    

    


