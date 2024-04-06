from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Length
from flask_wtf.file import FileField, FileAllowed,FileRequired

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[DataRequired(),InputRequired(),Length(max=700)])
    poster= FileField('Poster', validators=[FileRequired(),FileAllowed(["jpg","png","jpeg","Images only!"])])