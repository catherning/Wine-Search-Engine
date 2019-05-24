from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired 

class SearchBox(FlaskForm):
    query = StringField('WineSearch')#, validators=[DataRequired()])
    submit = SubmitField('Search')