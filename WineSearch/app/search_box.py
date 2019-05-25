from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired 

class SearchBox(FlaskForm):
    query = StringField('Describe the wine of your dreams...')#, validators=[DataRequired()])
    submit = SubmitField('I wanna get drunk with good wines!') #To change
    score_choices = [('Score','Above 50'),('Score','Above 75'),('Score','Above 90')]
    select = SelectField('Search for music:', choices=score_choices)