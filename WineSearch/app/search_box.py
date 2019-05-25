from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired,optional

class SearchBox(FlaskForm):
    query = StringField('WineSearch')#, validators=[DataRequired()])
    # score = SelectField('Score', choices=[('0','-'),('50','Above 50'),('75','Above 75'),('90','Above 90')],validators=[optional()])

    submit = SubmitField('Search')

