from flask import Flask, request, render_template, url_for, redirect, session
from forms import BasicForm
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

@app.route('/reset_session')
def reset_session():
    session['completed_exercises'] = []
    return redirect(url_for('show_exercise', question_id=0))

@app.route('/exercises/<int:question_id>', methods=['GET', 'POST'])
def show_exercise(question_id):
    # Session
    s = session['completed_exercises']
    print(s)

    form = BasicForm()
    multiple_choice_form = MultipleChoiceForm()
    conn = sqlite.create_connection('test.db')
    answer = form.basic_input.data
            
    question = sqlite.get_question_text(conn, question_id)
    ex_type = sqlite.get_exercise_type(conn, question_id)

    answers = [sqlite.get_answer(conn, question_id, i).casefold() for i in range(1, 4)]

    # go to a random exercise if you get this one right
    next_exercise_id = 0
    while(next_exercise_id == question_id or next_exercise_id in session['completed_exercises']):
        next_exercise_id = random.randint(0, sqlite.get_max_id(conn))
        print('Got a new random number: ', next_exercise_id)
    

    def completed_all_exercises():
        print('Num exercises: ', sqlite.get_max_id(conn) + 1)
        print('len(session[ting]): ', len(session['completed_exercises']))
        if sqlite.get_max_id(conn) == len(session['completed_exercises']):
            return 1
        return 0

    # User is presented with a multiple choice question
    if ex_type == 'MULTIPLE_CHOICE' and request.method == 'GET':
        correct_answer = answers[0]
        multiple_choice_form.choices = answers
        return render_template('multiple_choice.html', question=question,
                                                       multiple_choice_form=multiple_choice_form)
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
            
            print("This exercise ID: ", question_id)
            print("New exercise ID: ", next_exercise_id)
            if completed_all_exercises():
                return render_template('no_more_exercises.html', num_exercises=sqlite.get_max_id(conn))
            return redirect(url_for('show_exercise', question_id=next_exercise_id))
    
        else:
            return redirect(url_for('show_exercise', question_id=question_id))
    return render_template('level.html', form=form, question=question)


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