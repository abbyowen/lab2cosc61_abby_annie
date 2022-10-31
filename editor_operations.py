
# COSC 61, Professor Palmer 
# Authors: Abby Owen, Annie Revers
# editor_operations.py - SQL commands for editor operations

from cgi import test
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
        print(f"WELCOME EDITOR {row['EditorFirstName']} {row['EditorLastName']}".format(row))

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

########### schedule ###########
def schedule(mycursor, manuscript_id, issue_period, issue_year):
    try: 
        # check if status is ready, if not reject schedule
        ready_sql = "SELECT ManStatus, PageCount FROM Manuscript WHERE ManuscriptId = %s"
        val = (manuscript_id, )
        mycursor.execute(ready_sql, val)
        res = mycursor.fetchone()
        # get status of the manuscript and number of pages
        status = res[0]
        page = res[1]
        if status != "Ready":
            print("You cannot schedule a manuscript that is not in the \"Ready\" status.")
        else:
            # get issue id based off of the publication year and period number
            get_issue_id_sql = "SELECT IssueId FROM Issue WHERE PublicationYear = %s AND PeriodNumber = %s"
            issue_info = (issue_year, issue_period)
            mycursor.execute(get_issue_id_sql, issue_info)
            
            # get the issue id from the result
            res_issue_id = mycursor.fetchone()
            if res_issue_id == None:
                print("There is not issue with this publication year and publication period.")
            else:   
                # determine if the manuscript is full or not, or if adding this manuscript would make it overfill
                # if the number of pages in this manuscript plus the number of pages in the issue would overfill the issue
                issue_id = res_issue_id[0]   
                get_pages_sql = "SELECT PageCount FROM Issue WHERE IssueId = %s"
                issue = (issue_id, )
                mycursor.execute(get_pages_sql, issue)
                r = mycursor.fetchone()
                total_pages = r[0]
                # check the new page count
                if total_pages + page >= 100:
                    print("You cannot add this manuscript to this issue as doing so would result in an overfilled manuscript.")
                # add if the total pages will still be below 100
                else:
                    # update the manuscript to include the new issue id, the new status of scheduled, and the starting page which was the previous ending page of the issue
                    update_manuscript_sql = "UPDATE Manuscript SET IssueId = %s, StartingPage = %s, ManStatus = %s WHERE ManuscriptId = %s"
                    update_info = (issue_id, total_pages + 1, "Scheduled", manuscript_id)
                    mycursor.execute(update_manuscript_sql, update_info)
                    update_issue_pages_sql = "UPDATE Issue SET PageCount = %s WHERE IssueId = %s"
                    new_issue_info = (total_pages + page, issue_id)
                    mycursor.execute(update_issue_pages_sql, new_issue_info)

    except Error as err: 
        print(f"Error scheduling manuscript: {err}")

########### reset ###########
def reset(mycursor):
    try:
        # run the tables.sql files, which drops and recreates all of our tables
        f = open("tables.sql", "r")
        query = "".join(f.readlines())

        # go through each statement (delimited by a ; character)
        for s in query.split(";"):
            if len(s) > 0:
                mycursor.execute(s + ";")
        print("RESET COMPLETE: All tables dropped and recreated.")
        # recreate the triggers for new inserts 
        t = open("triggers.sql", "r")
        trigger_query = "".join(t.readlines())

        for s in trigger_query.split(";"):
            if len(s) > 0:
                print(s)
                mycursor.execute(s + ";", multi=True)
        
        # recreate the ICode table for new inserts
        query = "INSERT INTO ICode (InterestName) VALUES (\"ML\"), (\"english\"), (\"biology\"), (\"chemistry\"), (\"biology\"), (\"art history\"), (\"databases\"), (\"dartmouth\")"
        mycursor.execute(query)
        

      
    except Error as err:
        print(f"Error resetting system: {err}")

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

        check_review_count_sql = "SELECT COUNT(*) FROM Review WHERE ManuscriptId = %s AND A_Rating IS NOT NULL AND C_Rating IS NOT NULL AND M_Rating IS NOT NULL AND E_Rating IS NOT NULL AND Recommendation IS NOT NULL"
        check_vals = (manuscript_id, )
        mycursor.execute(check_review_count_sql, check_vals)
        res = mycursor.fetchone()
        if res[0] < 3:
            print("Not enough reviews on this manuscript to accept. Must have at least 3.")
        else:
            # update manuscript status to accepted
            query_1 = "UPDATE Manuscript SET ManStatus = 'Accepted' WHERE ManuscriptId = %s"
            values_1 = (manuscript_id, )
            mycursor.execute(query_1, values_1)

            # TEST CODE
            # print updated manuscript
            my_select2 = "SELECT * FROM Manuscript WHERE ManuscriptId = (%s)"
            vals4 = (manuscript_id,)
            mycursor.execute(my_select2, vals4)
            res2 = mycursor.fetchone()
            print(f"Manuscript {manuscript_id} has been Accepted! Now moving to the Typesetting and Ready statuses.")
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



    






    
    

        

    




    

    


