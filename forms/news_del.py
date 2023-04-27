from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Форма удаления новости
class NewsFormDel(FlaskForm):
    title = StringField('Номер новости', validators=[DataRequired()])
    submit = SubmitField('Удалить новость')
