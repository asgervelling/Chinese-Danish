import sqlite3
from app_dir.helpers import random_word

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=15)
    except sqlite3.Error as e:
        print(e)

    return conn

def print_all_questions():
    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")

    records = cur.fetchall()
    print('Total num rows: ', len(records))
    print('Printing each row:')
    for row in records:
        print('Question\t\t\t\t', row[0])
        print('Language:\t\t\t\t', row[1])
        print('Exercise type:\t\t\t\t', row[2])
        print('Text:\t\t\t\t\t', row[3])
        print()

    conn.close()

def print_all_answers():
    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ANSWERS")

    records = cur.fetchall()
    print('Total num rows: ', len(records))
    print('Printing each row:')
    for row in records:
        print('Answer\t\t\t\t', row[0])
        print('Answer 0\t\t\t\t', row[1])
        print('Answer 1\t\t\t\t', row[2])
        print('Answer 2\t\t\t\t', row[3])

    conn.close()
   
def get_question_text(id):
    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    records = cur.fetchall()
    conn.close()
    
    return records[id][3]

def get_answer(q_id, a_id):
    # This one needs a little work
    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ANSWERS")
    records = cur.fetchall()
    conn.close()

    return records[q_id][a_id]

def get_correct_index(q_id):
    conn = create_connection('test.db')
    cur = conn.cursor()
    # When you put the variable in a tuple with trailing commas,
    # SQLite3 escapes dangerous characters
    cur.execute("SELECT * FROM ANSWERS WHERE ID = ?", (q_id,))
    index = cur.fetchone()[4]
    conn.close()

    return index

def get_exercise_type(q_id):
    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    records = cur.fetchall()
    conn.close()

    return records[q_id][2]

def get_exercise_language(q_id):
    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    records = cur.fetchall()
    conn.close()

    return records[q_id][1]

def get_max_id():
    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute("SELECT MAX(ID) FROM QUESTIONS")
    
    records = cur.fetchone()
    max_id = records[0]

    conn.close()

    return max_id

def create_exercise_enter_the_answer(question:str,
                                     answer:str,
                                     language:str):
    conn = create_connection('test.db')
    cur = conn.cursor()
    ID = get_max_id() + 1

    # Add question to DB    
    cur.execute('INSERT INTO QUESTIONS (ID, LANG, EX_TYPE, TXT) ' \
                'VALUES (?, ?, "ENTER_THE_ANSWER", ?);', (ID, language, question))
    conn.commit()
    conn.close()

    conn = create_connection('test.db')
    cur = conn.cursor()

    # Add answer to DB
    cur.execute('INSERT INTO ANSWERS (ID, ANSWER_0, ANSWER_1, ANSWER_2, CORRECT_INDEX, POINTS_REWARD) ' \
                'VALUES (?, ?, ?, ?, -1, 10);', (ID, answer, random_word(16), random_word(16)))
    conn.commit()
    conn.close()

def create_exercise_multiple_choice(question:str,
                                    language:str,
                                    answer_0:str,
                                    answer_1:str,
                                    answer_2:str,
                                    correct_index:int):
    conn = create_connection('test.db')
    cur = conn.cursor()
    ID = get_max_id() + 1

    cur.execute('INSERT INTO QUESTIONS (ID, LANG, EX_TYPE, TXT) ' \
                'VALUES (?, ?, "MULTIPLE_CHOICE", ?);', (ID, language, question))
    conn.commit()
    conn.close()

    conn = create_connection('test.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO ANSWERS (ID, ANSWER_0, ANSWER_1, ANSWER_2, CORRECT_INDEX, POINTS_REWARD) ' \
                'VALUES (?, ?, ?, ?, ?, 10);', \
                (ID, answer_0, answer_1, answer_2, correct_index))
    conn.commit()

    conn.close()