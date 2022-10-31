from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
from ManUser import *

# TODO: File BLOBs for insert manuscript

########### register_editor ###########
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

########## login_editor ###########
def login_editor(mycursor, id): 
    q = "SELECT * FROM Editor WHERE EditorId = (%s)"
    val = int(id)
    try:
        mycursor.execute(q, (val,))
        row = dict(zip(mycursor.column_names, mycursor.fetchone()))
        print(f"WELCOME EDITOR {row['EditorFirstName']} {row['EditorLastName']}".format(row))
        
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




    






    
    

        

    




    

    


