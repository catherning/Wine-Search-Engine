from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, optional, NumberRange


class SearchBox(FlaskForm):
    query = StringField('')  # , validators=[DataRequired()])
    score = SelectField('Score (out of 100)',
                        choices=[('None', '-'),
                                 ('50', 'Above 50'),
                                 ('75', 'Above 75'),
                                 ('90', 'Above 90')])
    #score = StringField('Minimum score out of 100')
    # price= SelectField('Price (in $)',
    #                     choices=[('None', '-'),
    #                             ('20', 'Below 20'),
    #                             ('75', 'Above 75'),
    #                             ('90', 'Above 90')])

    price_l = IntegerField('Lowest price')  # TODO check max price ?
    price_h = IntegerField('Highest price')

    submit = SubmitField('Search')
