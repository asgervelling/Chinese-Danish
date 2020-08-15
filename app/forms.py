from flask_wtf import FlaskForm
from wtforms import StringField

class BasicForm(FlaskForm):
    basic_input = StringField('basic input', render_kw={'autofocus': True})