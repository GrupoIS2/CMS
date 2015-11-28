from flask.ext.wtf import Form  # RecaptchaField
from wtforms import TextField  # BooleanField
from wtforms import TextAreaField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from app.sections.models import Sections


def strip_filter(x):
    x.strip() if x else None


def section_choice():
    return Sections.query.all()


class ArticleCreateForm(Form):
    title = TextField('Title', [Required("Please enter a title")],
                      filters=[strip_filter])
    body = TextAreaField('Body', [Required("Please enter a body")],
                         filters=[strip_filter])
    section = QuerySelectField('Section', query_factory=section_choice)
    user_name = HiddenField()


class ArticleUpdateForm(Form):
    title = TextField('Title', [Required("Please enter a title")],
                      filters=[strip_filter])
    body = TextAreaField('Body', [Required("Please enter a body")],
                         filters=[strip_filter])
    section = QuerySelectField('Section', query_factory=section_choice)
    user_name = HiddenField()
    id_article = HiddenField()
