from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
from ManUser import *

# TODO: File BLOBs for insert manuscript

############## register_editor ##############
def register_editor(mycursor, firstname, lastname):
    try: 
        # insert user into the system
        query_1 = "INSERT INTO SysUser (UserType) VALUES (%s)reg"
        values_1 = ("editor", )
        mycursor.execute(query_1, values_1)
        
        # print user id
        id = mycursor.lastrowid
        print(f"Thank you for registering. Your editor ID is {id}.")
        
        # insert user into the editor table
        query_2 = "INSERT INTO Editor (EditorFirstName, EditorLastName, EditorId) VALUES (%s, %s, %s)"
        values_2 = (firstname, lastname, id)
        mycursor.execute(query_2, values_2)

        # return id 
        return id

    except Error as err:
        print(f"Error registering editor: {err}")
        return None

############# login_editor ##############
def login_editor(mycursor, id): 
    try:
        # log user into system
        query = "SELECT * FROM Editor WHERE EditorId = (%s)"
        values = int(id)
        mycursor.execute(query, (values,))
        row = dict(zip(mycursor.column_names, mycursor.fetchone()))
        
        # print welcome message
        print(f"WELCOME {row['EditorFirstName']} {row['EditorLastName']}".format(row))

        return row

    except Error as err:
        print(f"Error logging in editor: {err}")
        return None

########### editor_status ###########
def editor_status(mycursor):
    try:   
        # get all manuscripts in the system ordered by status and id
        print("######### MANUSCRIPT STATUSES #########")
        query_1 = "SELECT * FROM AnyAuthorManuscripts ORDER BY ManStatus ASC, ManuscriptId ASC"
        mycursor.execute(query_1)
        res = mycursor.fetchall()

        # print all manuscripts
        for manuscript in res: 
            print(manuscript)

    except Error as err:
        print(f"Error getting manuscript statuses: {err}")
    
########### assign ###########
def assign(mycursor, reviewer_id, manuscript_id):
    try:    
        # insert user into the review table
        query_1 = "INSERT INTO Review (ReviewerId, ManuscriptId) VALUES (%s, %s)"
        values_1 = (int(reviewer_id), int(manuscript_id))
        mycursor.execute(query_1, values_1)

        ######
        # TEST CODE REMOVE BEFORE SUBMISSION
        # print last review inserted
        my_select = "SELECT * FROM Review WHERE ReviewerId = %s AND ManuscriptId = %s"
        vals3 = (reviewer_id, manuscript_id)
        mycursor.execute(my_select, vals3)
        res = mycursor.fetchone()
        print(res)
        # 60
        # 11
        ######

        # update manuscript status to under review
        query_2 = "UPDATE Manuscript SET ManStatus = 'under review' WHERE ManuscriptId = %s"
        values_2 = (manuscript_id, )
        mycursor.execute(query_2, values_2)

        #######
        ### TEST CODE REMOVE
        # print updated manuscript
        my_select2 = "SELECT * FROM Manuscript WHERE ManuscriptId = (%s)"
        vals4 = (manuscript_id,)
        mycursor.execute(my_select2, vals4)
        res2 = mycursor.fetchone()
        print(res2)
        #######
        
    except Error as err:
        print(f"Error assigning manuscript to reviewer: {err}")

########### editor_accept ###########
def editor_accept(mycursor, manuscript_id):
    try:    
        # update manuscript status to accepted
        query_1 = "UPDATE Manuscript SET ManStatus = 'accepted' WHERE ManuscriptId = %s"
        values_1 = (manuscript_id, )
        mycursor.execute(query_1, values_1)

        # TEST CODE
        # print updated manuscript
        my_select2 = "SELECT * FROM Manuscript WHERE ManuscriptId = (%s)"
        vals4 = (manuscript_id,)
        mycursor.execute(my_select2, vals4)
        res2 = mycursor.fetchone()
        print(res2)
    except Error as err:
        print(f"Error updating manuscript status to accepted: {err}")

########### editor_reject ###########
def editor_reject(mycursor, manuscript_id):
    try:    
        # update manuscript status to rejected
        query_1 = "UPDATE Manuscript SET ManStatus = 'rejected' WHERE ManuscriptId = %s"
        values_1 = (manuscript_id, )
        mycursor.execute(query_1, values_1)

        #######
        # TEST CODE
        # print updated manuscript
        my_select2 = "SELECT * FROM Manuscript WHERE ManuscriptId = (%s)"
        vals4 = (manuscript_id,)
        mycursor.execute(my_select2, vals4)
        res2 = mycursor.fetchone()
        print(res2)
    except Error as err:
        print(f"Error setting manuscript stauts to rejected: {err}")

########### publish ###########
def publish(mycursor, issue_id):
    try:    
        # update status of manuscripts with this issue id to published
        query = "UPDATE Manuscript SET ManStatus = 'Published' WHERE IssueId = %s"
        variables= (issue_id,)
        mycursor.execute(query, variables)

        # TEST CODE
        # print updated manuscript
        # print updated manuscript
        my_select2 = "SELECT * FROM Manuscript WHERE IssueId = %s"
        mycursor.execute(my_select2, variables)
        print(mycursor.fetchone())
    except Error as err:
        print(f"Error publishing issue: {err}")


    






    
    

        

    




    

    


