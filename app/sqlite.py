import sqlite3
from sqlite3 import Error

'''

    To do:
    Load less data when reading from the database.

'''

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
    cur.execute("SELECT * FROM ANSWERS_old")

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

    return records[q_id][a_id].casefold() ## get more answers, if any

def get_correct_index(conn, q_id):
    cur = conn.cursor()
    query = "SELECT * FROM ANSWERS WHERE ID = {}".format(q_id)
    cur.execute(query)
    index = cur.fetchone()[4]

    print('Correct answer index: ', index)
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
    print('Printing {} with {} items'.format(table_name, num_items))

    for variable, datatype in variables_with_types:
        row_string = variable + ' ' + datatype + ' NOT NULL,\n'
        # Make IDs unique
        if variable in ['ID', 'Id', 'iD', 'id']:
            row_string = variable + ' ' + datatype + ' PRIMARY KEY NOT NULL,\n'
        
        # remove the last command and new line
        if index >= num_items - 1:
            row_string = row_string[:-2]
        print('Index: ', index)
        query += row_string
        index += 1
    query += ');'
    print(query)

    cur.execute(query)
    
def create_question(conn, question:str, answer:str):
    pass



# Run these functions on startup
conn = create_connection('test.db')
with conn:
    create_table_if_not_exists(conn,
                            'QUESTIONS',
                            ('ID', 'INT'),
                            ('LANG', 'TEXT'),
                            ('EX_TYPE', 'TEXT'),
                            ('TXT', 'TEXT'))
    create_table_if_not_exists(conn,
                            'ANSWERS',
                            ('ID', 'INT'),
                            ('ANSWER', 'TEXT'),
                            ('ALTERNATIVE_ANSWER', 'TEXT'),
                            ('CORRECT_INDEX', 'INT'),
                            ('POINTS_REWARD', 'INT'))
    print_all_answers(conn)
    conn.commit()