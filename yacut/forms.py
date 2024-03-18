from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 180)]
    )
    custom_id = URLField(
        'Введите ваш вариант кастомной ссылки',
        validators=[Length(0, 16), Optional()]
    )
    submit = SubmitField('Создать')