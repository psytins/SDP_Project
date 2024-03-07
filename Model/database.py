import mysql.connector
from mysql.connector import Error
from Application.encryption import *

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="password",
            database="notes"
        )
        return connection
    except Error as err:
        print(f"Error connecting to the database {err}")
        return None

def perform_query(query, params=()):
    db_connection = create_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        try:
            cursor.execute(query, params)
            db_connection.commit()
            cursor.close()
            db_connection.close()
        except Error as err:
            print(f"Error connecting to the database {err}")
            return None

def perform_search_query(query, params=()):
    db_connection = create_db_connection()
    if db_connection is not None:
        cursor = db_connection.cursor()
        try:
            cursor.execute(query, params)
            records = cursor.fetchall()
            db_connection.commit()
            cursor.close()
            db_connection.close()

            return records
        except Error as err:
            print(f"Error connecting to the database {err}")
            return None

# Database - Notes
def bd_insert_note(title, body, user_id):
    query = "INSERT INTO note (title, description, user_id) VALUES (%s, %s, %s)"
    return perform_query(query, (encrypt(title), encrypt(body), user_id))

def bd_get_notes(user_id):
    query = "SELECT id, title, description FROM note WHERE user_id = %s"
    query_results = perform_search_query(query, (user_id,))

    results = list()
    for i in query_results:
        l = list(i)
        l[0] = l[0]          #id
        l[1] = decrypt(l[1]) #title
        l[2] = decrypt(l[2]) #body

        results.append(tuple(l))

    return results

def bd_get_note(note_id, user_id):
    query = "SELECT id, title, description FROM note WHERE id = %s and user_id = %s"
    query_results = perform_search_query(query, (note_id,user_id))

    results = list()
    for i in query_results:
        l = list(i)
        l[0] = l[0]             #id
        l[1] = decrypt(l[1])    #title
        l[2] = decrypt(l[2])    #body

        results.append(tuple(l))
        
    return results


def bd_delete_note(note_id, user_id):
    query = "DELETE FROM note WHERE id = %s AND user_id = %s"
    return perform_query(query, (note_id, user_id))

# Database - User
def bd_insert_user(username, password):
    query = "INSERT INTO user (username, password) VALUES (%s, %s)"
    return perform_query(query, (username, encrypt(password)))

def bd_search_user(username, get = 0): # return id of user if founded. Return -1 if not founded. get can be 0(id), 1(username) and 2(password)
    query = f"SELECT * FROM user where username = '{username}'"
    res = perform_search_query(query)

    if(len(res) == 0):
        return -1
    else:
        if(get == 0 or get == 1 or get == 2):
            if(get == 0):
                return int(res[0][get]) # return id
            else:
                return res[0][get] # return according to get param
        else:
            print("Select the right get index.")