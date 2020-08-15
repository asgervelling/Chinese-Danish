from flask import Flask, request, render_template, url_for, redirect
from forms import BasicForm

import sqlite3
from sqlite3 import Error

import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return render_template('index.html')
    
questions = {
    '2 + 2 = __': '4',
    'Hvem er præsident i USA?': 'Donald Trump'
}

@app.route('/levels/<int:lvl>', methods=['GET', 'POST'])
def show_level(lvl):
    form = BasicForm()
    if lvl >= len(questions):
        return redirect('/HTTP_error/404')
    question = list(questions.keys())[lvl]
    next_level = '/levels/' + str(lvl+1)
    if form.basic_input.data == questions[question]:
        return redirect(next_level)
    
    return render_template('level.html', form=form, question=question)

@app.route('/HTTP_error/<int:error_code>')
def HTTP_error_page(error_code):
    return render_template('HTTP_error.html', error_code=error_code)

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