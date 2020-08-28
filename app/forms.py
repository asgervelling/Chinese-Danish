from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

class BasicForm(FlaskForm):
    basic_input = StringField('basic input', render_kw={'autofocus': True})

class MultipleChoiceForm(FlaskForm):
    answers = SelectField('multiple_choice')

class AddExerciseFormEnterTheAnswer(FlaskForm):
    question = StringField('question input')
    lang = StringField('lang input')
    answer_0 = StringField('answer_0')
    answer_1 = StringField('answer_1')
    answer_2 = StringField('answer_2')
    ex_type = StringField('ex_type')

class AddExerciseFormMultipleChoice(FlaskForm):
    question = StringField('question input')
    lang = StringField('lang input')
    answer_0 = StringField('answer_0')
    answer_1 = StringField('answer_1')
    answer_2 = StringField('answer_2')
    ex_type = StringField('ex_type')
    correct_index = StringField('correct_index')