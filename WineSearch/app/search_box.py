from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange


class SearchBox(FlaskForm):
    query = StringField('', render_kw={"placeholder": '"dom perignon 2010","red france cherry smoked"'})  # , validators=[DataRequired()])
    score = SelectField('Score (out of 100)',validators=[Optional()],
                        choices=[('None', '-'),
                                 ('50', 'Above 50'),
                                 ('75', 'Above 75'),
                                 ('90', 'Above 90')],)
    #score = StringField('Minimum score out of 100')
    # price= SelectField('Price (in $)',
    #                     choices=[('None', '-'),
    #                             ('20', 'Below 20'),
    #                             ('75', 'Above 75'),
    #                             ('90', 'Above 90')])

    price_l = IntegerField('Lowest price',validators=[Optional()])  # TODO check max price ?
    price_h = IntegerField('Highest price',validators=[Optional()])

    submit = SubmitField('Search')
