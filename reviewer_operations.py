from mysql.connector import MySQLConnection, Error, errorcode, FieldType
from dbconfig import read_db_config
import getpass
from ManUser import *

def register_reviewer(mycursor, words, icodes):

    print(words)
    
    q1 = "INSERT INTO Reviewer (ReviewerFirstName ReviewerLastName) VALUES (%s, %s)"
    val = (words[2], words[3])
    try: 
        mycursor.execute(q1, val)
        id = mycursor.lastrowid
        print(f"Thank you for registering. Your editor ID is {id}")

        for c in icodes:
            reviewer_icode_group = "INSERT INTO ReviewerICodeGroup (ReviewerId, ICodeId) VALUES (%s, %s)"
            v = (id, c)
            mycursor.execute(reviewer_icode_group, v)

        return id
    except Error as err:
        print(err.msg)
        print(f"Error registering editor: {err}")

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

