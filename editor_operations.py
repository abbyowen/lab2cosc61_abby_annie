from mysql.connector import Error
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
        print(f"WELCOME EDITOR {row['EditorFirstName']} {row['EditorLastName']}".format(row))

        
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

def schedule(mycursor, manuscript_id, issue_period, issue_year):
    try: 
        # check if ready 
        ready_sql = "SELECT ManStatus, PageCount FROM Manuscript WHERE ManuscriptId = %s"
        val = (manuscript_id, )
        mycursor.execute(ready_sql, val)
        res = mycursor.fetchone()
        status = res[0]
        page = res[1]
        if status != "Ready":
            print("You cannot schedule a manuscript that is not in the \"Ready\" status.")
        else:
            # get issue id 
            get_issue_id_sql = "SELECT IssueId FROM Issue WHERE PublicationYear = %s AND PeriodNumber = %s"
            issue_info = (issue_year, issue_period)
            mycursor.execute(get_issue_id_sql, issue_info)
            
            res_issue_id = mycursor.fetchone()
            if res_issue_id == None:
                print("There is not issue with this publication year and publication period.")
            else:   
                issue_id = res_issue_id[0]   


                get_pages_sql = "SELECT PageCount FROM Issue WHERE IssueId = %s"
                issue = (issue_id, )
                mycursor.execute(get_pages_sql, issue)
                r = mycursor.fetchone()
                total_pages = r[0]
                if total_pages + page > 100:
                    print("You cannot add this manuscript to this issue as doing so would result in an overfilled manuscript.")
                else:
                    update_manuscript_sql = "UPDATE Manuscript SET IssueId = %s, StartingPage = %s, ManStatus = %s WHERE ManuscriptId = %s"
                    update_info = (issue_id, total_pages + 1, "Scheduled", manuscript_id)
                    mycursor.execute(update_manuscript_sql, update_info)
                    update_issue_pages_sql = "UPDATE Issue SET PageCount = %s WHERE IssueId = %s"
                    new_issue_info = (total_pages + page, issue_id)
                    mycursor.execute(update_issue_pages_sql, new_issue_info)

    except Error as err: 
        print(f"Error scheduling manuscript: {err}")

def reset(mycursor):
    try:
        f = open("tables.sql", "r")
        query = "".join(f.readlines())

        for statement in query.split(";"):
            if len(statement) > 0:
                mycursor.execute(statement + ";")
        print("RESET COMPLETE: All tables dropped and recreated.")

        
    except Error as err:
        print(f"Error resetting system: {err}")


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



    






    
    

        

    




    

    


