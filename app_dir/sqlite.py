import sqlite3
import string
import random

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

def print_all_questions(conn):
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

def print_all_answers(conn):
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

def get_question_records(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    records = cur.fetchall()

    return records
   
def get_question_text(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    records = cur.fetchall()
    
    return records[id][3]

def get_answer(conn, q_id, a_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM ANSWERS")
    records = cur.fetchall()

    return records[q_id][a_id]

def get_correct_index(conn, q_id):
    cur = conn.cursor()
    query = "SELECT * FROM ANSWERS WHERE ID = {}".format(q_id)
    cur.execute(query)
    index = cur.fetchone()[4]

    return index

def get_exercise_type(conn, q_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    records = cur.fetchall()

    return records[q_id][2]

def get_exercise_language(conn, q_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    records = cur.fetchall()

    return records[q_id][1]

def get_max_id(conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(ID) FROM QUESTIONS")
    
    records = cur.fetchone()
    max_id = records[0]

    return max_id

def create_table_if_not_exists(conn, table_name:str, *variables_with_types:tuple):
    cur = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS {}\n(".format(table_name)
    
    num_items = len(variables_with_types)
    index = 0

    for variable, datatype in variables_with_types:
        row_string = variable + ' ' + datatype + ' NOT NULL,\n'
        # Make IDs unique
        if variable in ['ID', 'Id', 'iD', 'id']:
            row_string = variable + ' ' + datatype + ' PRIMARY KEY NOT NULL,\n'
        
        # remove the last command and new line
        if index >= num_items - 1:
            row_string = row_string[:-2]
        query += row_string
        index += 1
    query += ');'

    cur.execute(query)
    
def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_exercise_enter_the_answer(question:str,
                                     answer:str,
                                     language:str):
    conn = create_connection('test.db')
    cur = conn.cursor()
    ID = get_max_id(conn) + 1

    # Questions table
    q_query = 'INSERT INTO QUESTIONS (ID, LANG, EX_TYPE, TXT) ' \
              'VALUES ({}, "{}", "ENTER_THE_ANSWER", "{}");'.format(ID, language, question)

    # Answers table
    a_query = 'INSERT INTO ANSWERS (ID, ANSWER_0, ANSWER_1, ANSWER_2, CORRECT_INDEX, POINTS_REWARD) ' \
              'VALUES ({}, "{}", "{}", "{}", -1, 10);'.format(ID, answer, random_word(16), random_word(16))

    cur.execute(q_query)
    conn.commit()

    cur.execute(a_query)
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
    ID = get_max_id(conn) + 1

    q_query = 'INSERT INTO QUESTIONS (ID, LANG, EX_TYPE, TXT) ' \
              'VALUES ({}, "{}", "MULTIPLE_CHOICE", "{}");'.format(ID, language, question)
    
    a_query = 'INSERT INTO ANSWERS (ID, ANSWER_0, ANSWER_1, ANSWER_2, CORRECT_INDEX, POINTS_REWARD) ' \
              'VALUES ({}, "{}", "{}", "{}", {}, 10);' \
              .format(ID, answer_0, answer_1, answer_2, correct_index)

    cur.execute(q_query)
    conn.commit()

    cur.execute(a_query) # ACID???
    conn.commit()

    conn.close()