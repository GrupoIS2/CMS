from flask.ext.wtf import Form  # RecaptchaField
from wtforms import StringField, TextAreaField  # BooleanField
from wtforms.validators import DataRequired


class CreateSectionForm(Form):
    section = StringField('section', validators=[DataRequired()])
    description = TextAreaField('description')


class EditSectionForm(Form):
    section = StringField('section', validators=[DataRequired()])
    description = TextAreaField('description')
