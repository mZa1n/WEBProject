from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Форма выдачи админ-прав
class GiveAdmin(FlaskForm):
    id = StringField('ID пользователя', validators=[DataRequired()])
    submit = SubmitField('Выдать')
