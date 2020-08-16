from flask import Flask, request, render_template, url_for, redirect, session
from forms import BasicForm
from pinyin import get
import random

import sqlite
from forms import *

import os

app = Flask(__name__)
app.secret_key = 'this_is_secret'
app.static_folder = 'static'

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/select_language/<language>')
def select_language(language):
    session['client_language'] = language
    if session['client_language'] == 'ZH-DA':
        return redirect('/exercises/0')
    return redirect('/exercises/2')

@app.route('/reset_session')
def reset_session():
    session['completed_exercises'] = []
    return redirect(url_for('show_exercise', question_id=0))

@app.route('/test_demo')
def test_demo():
    return render_template('testing.html')

@app.route('/exercises/<int:question_id>', methods=['GET', 'POST'])
def show_exercise(question_id):
    form = BasicForm()
    multiple_choice_form = MultipleChoiceForm()
    conn = sqlite.create_connection('test.db')
    answer = form.basic_input.data
            
    question = sqlite.get_question_text(conn, question_id)

    if 'completed_exercises' in session:
        compl_ex_list = session['completed_exercises']
        if not question_id in compl_ex_list:
            compl_ex_list.append(question_id)
            session['completed_exercises'] = compl_ex_list
    else:
        session['completed_exercises'] = []

    def get_DA_ZH_html(string:str):
        ''' Use for strings like "Han ser meget [电视]" '''
        pinyin_mode = False
        chinese = ''
        danish = ''
        danish_a = ''
        danish_b = ''
        chinese_insert_index = 0
        html = ''
        for char in string:
            if char == '[':
                pinyin_mode = True
                chinese_insert_index = len(danish)
            if char == ']':
                chinese += char
                pinyin_mode = False
                continue
            if pinyin_mode == True:
                chinese += '<div class="tooltip">{}<span class="tooltiptext">{}</span></div>'.format(char, get(char))
                continue
            if pinyin_mode == False:
                danish += char

        danish_a = danish[:chinese_insert_index]
        danish_b = danish[chinese_insert_index:]
        html = danish_a + chinese + danish_b
        return(html)

    def get_ZH_DA_html(string:str):
        ''' Use for strings like 我听不[forstå] '''
        pinyin_mode = True
        chinese = ''
        chinese_a = ''
        chinese_b = ''
        danish = ''
        danish_insert_index = 0
        question_html = ''
        
        for char in string:
            if char == '[':
                pinyin_mode = False
                danish_insert_index = len(chinese)
            if char == ']':
                danish += char
                pinyin_mode = True
                continue
            if pinyin_mode == True:
                chinese += '<div class="tooltip">{}<span class="tooltiptext">{}</span></div>'.format(char, get(char))
                continue
            if pinyin_mode == False:
                danish += char

        # Build entire HTML string
        chinese_a = chinese[:danish_insert_index]
        chinese_b = chinese[danish_insert_index:]
        question_html = chinese_a + danish + chinese_b
        return question_html
        

    # Question, exercise type, language and answers
    ex_lang = sqlite.get_exercise_language(conn, question_id)
    question_html = ''
    if (ex_lang == 'DA-ZH'): 
        question_html = get_ZH_DA_html(question)

    if (ex_lang == 'ZH-DA'):
        question_html = get_DA_ZH_html(question)
    
    

    ex_type = sqlite.get_exercise_type(conn, question_id)
    answers = [sqlite.get_answer(conn, question_id, i).casefold() for i in range(1, 4)]

    # go to a random exercise if you get this one right
    next_exercise_id = 0
    while(next_exercise_id == question_id or next_exercise_id in session['completed_exercises']):
        next_exercise_id = random.randint(0, sqlite.get_max_id(conn))  

    def completed_all_exercises():
        if sqlite.get_max_id(conn) == len(session['completed_exercises']):
            return 1
        return 0


    ''' GET '''  
    # User is presented with a multiple choice question
    if ex_type == 'MULTIPLE_CHOICE' and request.method == 'GET':
        correct_answer = answers[0]
        multiple_choice_form.choices = answers
        return render_template('multiple_choice.html', question_html=question_html,
                                                       multiple_choice_form=multiple_choice_form)

    if ex_type == 'ENTER_THE_ANSWER' and request.method == 'GET':
        if (ex_lang == 'DA-ZH'): 
            question_html = question

        if (ex_lang == 'ZH-DA'):
            question_html = get_ZH_DA_html(question)
            
            
        return render_template('level.html', question_html=question_html,
                                             form=form)

    ''' POST '''
    # User attempts to solve an exercise                                                   
    if request.method == 'POST':
        # 'MULTIPLE_CHOICE' exercise
        if ex_type == 'MULTIPLE_CHOICE':
            correct_answer = answers[0]
            button_input = request.form.to_dict()
            
            # Correct answer
            if correct_answer in button_input:
                # Don't show the same question twice in the same session
                if 'completed_exercises' in session:
                    compl_ex_list = session['completed_exercises']
                    if not question_id in compl_ex_list:
                        compl_ex_list.append(question_id)
                        session['completed_exercises'] = compl_ex_list
                else:
                    session['completed exercises'] = [question_id]

                if completed_all_exercises():
                    return render_template('no_more_exercises.html', num_exercises=sqlite.get_max_id(conn))
                return redirect(url_for('show_exercise', question_id=next_exercise_id))
            # Wrong answer
            else:
                return redirect(url_for('show_exercise', question_id=question_id))
        
        # 'ENTER_THE_ANSWER' exercise
        text_input = form.basic_input.data
        if text_input in answers:
            # Don't show the same question twice in the same session
            if 'completed_exercises' in session:
                compl_ex_list = session['completed_exercises']
                if not question_id in compl_ex_list:
                    compl_ex_list.append(question_id)
                    session['completed_exercises'] = compl_ex_list
            else:
                session['completed exercises'] = [question_id]
            
            if completed_all_exercises():
                return render_template('no_more_exercises.html', num_exercises=sqlite.get_max_id(conn))
            return redirect(url_for('show_exercise', question_id=next_exercise_id))
    
        else:
            return redirect(url_for('show_exercise', question_id=question_id))


    
    return render_template('level.html', form=form, question_html=question_html)


@app.route('/app', methods=['GET','POST'])
def app_page():
    if request.method == 'GET':
        return redirect('/exercises/0')
    else:
        return 'post request on /app'

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)