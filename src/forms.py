from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class SearchForm(Form):
    src = StringField('From', validators=[DataRequired()])
    dst = StringField('To', validators=[DataRequired()])
