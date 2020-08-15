from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

class BasicForm(FlaskForm):
    basic_input = StringField('basic input', render_kw={'autofocus': True})

class MultipleChoiceForm(FlaskForm):
    answers = SelectField('multiple_choice')