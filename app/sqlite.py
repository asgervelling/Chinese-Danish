import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def print_all_questions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTION")

    records = cur.fetchall()
    print('Total num rows: ', len(records))
    print('Printing each row:')
    for row in records:
        print('Question\t\t\t\t', row[0])
        print('Language:\t\t\t\t', row[1])
        print('Exercise type:\t\t\t\t', row[2])
        print('Text:\t\t\t\t\t', row[3])
        print()

def print_all_answers(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ANSWER")

    records = cur.fetchall()
    print('Total num rows: ', len(records))
    print('Printing each row:')
    for row in records:
        print('Answer\t\t\t\t', row[0])
        print('Answer 0\t\t\t\t', row[1])
        print('Answer 1\t\t\t\t', row[2])
        print('Answer 2\t\t\t\t', row[3])
   
def get_question_text(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTION")
    records = cur.fetchall()
    
    return records[id][3]

def get_answer(conn, q_id, a_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ANSWER")
    records = cur.fetchall()

    return records[q_id][a_id]

def get_exercise_type(conn, q_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTION")
    records = cur.fetchall()

    return records[q_id][2]

def correct_answer(conn, q_id, answer:str):
    # answers = [1, 2, 3]
    for i in range(1, 4):
        accepted_answer = get_answer(conn, q_id, i)
        print('accepted answer: ', accepted_answer)
        print('your answer: ', answer)
        if answer == accepted_answer:
            print('That is correct')
            return True
    return False

conn = create_connection('test.db')
with conn:
    print_all_questions(conn)
    print(get_question_text(conn, 3))
    correct_answer(conn, 3, 'paobu')