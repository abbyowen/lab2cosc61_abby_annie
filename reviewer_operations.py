from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
from ManUser import *

def register_reviewer(mycursor, first, last, icodes):
    
    q1 = "INSERT INTO Reviewer (ReviewerFirstName ReviewerLastName) VALUES (%s, %s)"
    val = (first, last)
    try: 
        mycursor.execute(q1, val)
        id = mycursor.lastrowid
        print(f"Thank you for registering. Your reviewer ID is {id}")

        for c in icodes:
            reviewer_icode_group = "INSERT INTO ReviewerICodeGroup (ReviewerId, ICodeId) VALUES (%s, %s)"
            v = (id, c)
            mycursor.execute(reviewer_icode_group, v)

        return id
    except Error as err:
        print(err.msg)
        print(f"Error registering editor: {err}")

def reviewer_login(mycursor, rev_id):
    get_mans(mycursor, rev_id)
    q1 = "SELECT a.ManuscriptId, Title, ManStatus FROM (SELECT ManuscriptId, Title FROM ReviewStatus) a LEFT JOIN (SELECT ManuscriptId, ManStatus FROM Manuscript) b ON a.ManuscriptId = b.ManuscriptId ORDER BY FIELD(ManStatus, \"Under Review\", \"Accepted\", \"Rejected\")"

    try: 
        mycursor.execute(q1)
        res = mycursor.fetchall()
        for x in res:
            print(x)
        
    except Error as err:
        print(f"Error logging in reviewer: {err}")

def get_mans(mycursor, rev_id):
    set_id = "SET @rev_id = %s"
    vals = (rev_id, )

    try:
        mycursor.execute(set_id, vals)
    except Error as err:
        print(f"Error setting reviewer id: {err}")


def man_review(mycursor, user, scores, man_id, decision):
    if user.get_id() == None:
        print("You do not have the proper permissions for this action. Please log in with you Author ID to submit a manuscript.")


    check_manuscript_sql = "SELECT EXISTS(SELECT 1 FROM Review WHERE ManuscriptId = %s AND ReviewerId = %s)"
    val = (man_id, user.get_id())
    try: 
        mycursor.execute(check_manuscript_sql, val)
        res = mycursor.fetchone()
        if res[0] == 0:
            print("You are not assigned to review this manuscript.")
            return
    except Error as err:
        print(f"Error checking reviews: {err}")
    
    
    accept_sql = "UPDATE Review SET A_Rating = %s, C_Rating = %s, M_Rating = %s, E_Rating = %s, Recommendation = %s WHERE ManuscriptId = %s AND ReviewerId = %s"
    vals = (scores["A"], scores["C"], scores["M"], scores["E"], decision, man_id, user.get_id()) 
    try: 
        mycursor.execute(accept_sql, vals)
    except Error as err: 
        print(f"Error updating review: {err}")

