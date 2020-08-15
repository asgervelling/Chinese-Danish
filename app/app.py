from flask import Flask, request, render_template, url_for, redirect
from forms import BasicForm



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

exercises = {
    # type of exercise: {language to language: {specific exercise: {correct answers: list[]}}}
    'enter_the_answer': {
        'da-zh': {
            'Hvordan siger man "kaffe" på kinesisk?': ['咖啡', 'kafei', 'ka fei'],
            'Hvordan siger man "at løbe" på kinesisk?': ['跑步', 'paobu', 'pao bu']
        },
        'zh-da': {
            '用丹麦语怎么说 咖啡？': ['kaffe', 'Kaffe'],
            '用丹麦语怎么说 跑步？': ['at løbe', 'løbe']
        }
    },
    'multiple_choice': {
        'da-zh': {
            '小名的[ven]要去超市买东西': ['朋友', 'pengyou', 'peng you'],
            '她喜欢看[fjernsyn]': ['电视', 'dianshi', 'dian shi']
        },
        'zh-da':
        {
            'Christians [朋友] tager i supermarkedet for at købe ind': ['ven', 'Ven']
        }
    }
}





@app.route('/exercises/<string:type_of_exercise>/<string:lang>/<int:question_id>', methods=['GET', 'POST'])
def show_exercise(type_of_exercise, lang, question_id):
    form = BasicForm()
    question = ''
    answer = ''
    index = 0
    for q, a in exercises['multiple_choice']['da-zh'].items():
        for answer in a:
            print(answer)
        if index == int(question_id):
            question = q
            print('QUESTION: ', question)
            break
        index += 1
    e = exercises[type_of_exercise][lang].items()
    if request.method == 'POST':
        answer = form.basic_input.data
        print('The answer is ', answer)
    for a, b in e:
        print(b)
    print('Question: ', question)

    

    correct = False
    def correct_answer():
        for q, a in exercises[type_of_exercise][lang].items():
            
        
            print('{{')
            print(q)
            print(a)
            if answer in a:
                correct = True
                print('it is trueeeeeeeeeeeeee')
            else:
                print('it is not true. answer:')
                print(answer)
    
    correct_answer()     
    
    if correct == True:
        print('correct answer')
        next_question = 'exercises/' + type_of_exercise + '/' \
                                      + lang + '/' + str(question_id)
        print(next_question)
        return redirect(next_question)
        print('Question ID == ', question_id)
        
        return redirect(url_for('show_exercise', type_of_exercise=type_of_exercise,
                                               lang=lang,
                                               question_id=1))
    else:
        print('not correct\n_________________________')
        
    
    return render_template('level.html', form=form, question=question)
    
    # question to display
    
    
    

    return 'hi'


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