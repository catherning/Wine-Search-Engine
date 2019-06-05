from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Optional, NumberRange


class SearchBox(FlaskForm):
    query = StringField('', render_kw={"placeholder": '"dom perignon","red cherry smoked 2010"'})  # , validators=[DataRequired()])
    score = SelectField('Score (out of 100)',validators=[Optional()],
                        choices=[('None', '-'),
                                 ('50', 'Above 50'),
                                 ('75', 'Above 75'),
                                 ('90', 'Above 90')],)


    price_l = FloatField('price_l',validators=[Optional()])  # TODO check max price ?
    price_h = FloatField('price_h',validators=[Optional()])
    #TODO check if people enter not integers
    
    submit = SubmitField('Search')
