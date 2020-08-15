from flask import Flask, request, render_template, url_for, redirect
from forms import BasicForm

import sqlite
from forms import *

import os

app = Flask(__name__)
app.secret_key = 'this_is_secret'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exercises/<int:question_id>', methods=['GET', 'POST'])
def show_exercise(question_id):
    form = BasicForm()
    multiple_choice_form = MultipleChoiceForm()
    conn = sqlite.create_connection('test.db')
    answer = form.basic_input.data
            
    question = sqlite.get_question_text(conn, question_id)
    ex_type = sqlite.get_exercise_type(conn, question_id)

    answer_0 = sqlite.get_answer(conn, question_id, 1).casefold()
    answer_1 = sqlite.get_answer(conn, question_id, 2).casefold()
    answer_2 = sqlite.get_answer(conn, question_id, 3).casefold()
    answers = [answer_0, answer_1, answer_2]

    if ex_type == 'MULTIPLE_CHOICE' and request.method == 'GET':
        correct_answer = answer_0
        multiple_choice_form.choices = answers
        return render_template('multiple_choice.html', question=question,
                                                       multiple_choice_form=multiple_choice_form)
    if request.method == 'POST':
        if ex_type == 'MULTIPLE_CHOICE':
            correct_answer = answer_0
            if 'a_0' in request.form:
                print("it is in it yes")
            button_input = request.form.to_dict()
            print(button_input.keys())
            print(correct_answer)
            if correct_answer in button_input:
                return redirect(url_for('show_exercise', question_id=question_id+1))
            else:
                return redirect(url_for('show_exercise', question_id=question_id))
        # User just typed something into the text field
        text_input = form.basic_input.data
        print('text input: ', text_input, answers)
        if text_input in answers:
            return redirect(url_for('show_exercise', question_id=question_id+1))
        

    
    return render_template('level.html', form=form, question=question)
    



@app.route('/levels/<int:lvl>', methods=['GET', 'POST'])
def show_level(lvl):
    form = forms.BasicForm()
    if lvl >= len(questions):
        return redirect('/HTTP_error/404')
    question = list(questions.keys())[lvl]
    next_level = '/levels/' + str(lvl+1)
    if form.basic_input.data == questions[question]:
        return redirect(next_level)    
    return render_template('level.html', form=form, question=question)



@app.errorhandler(404)
def not_found(error):
    return render_template('HTML_error.html'), 404

@app.route('/app', methods=['GET','POST'])
def app_page():
    if request.method == 'GET':
        return redirect('/levels/0')
    else:
        return 'hello'

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)