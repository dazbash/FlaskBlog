from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title = StringField(validators=DataRequired())
    summary = TextAreaField()
    content = TextAreaField(validators=DataRequired())
    slug = StringField(validators=DataRequired())