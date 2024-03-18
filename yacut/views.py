from flask import abort, flash, redirect, render_template, url_for, request

from . import app, db
from .forms import URLForm
from .models import URL_map

import random, string


def get_random_string(length=8):
    """Генерирует случайную строку заданной длины."""

    allowed_characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(allowed_characters) for _ in range(length))

    return random_string


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    base_url = request.base_url
    form = URLForm()

    if form.validate_on_submit():
        if form.custom_id.data:
            short = form.custom_id.data
            if URL_map.query.filter_by(short=short).first():
                flash('Этот идентификатор уже занят!', 'duplicate-message')
                return render_template('yacut.html', form=form)
        else:
            short = get_random_string()

        url = URL_map(original=form.original_link.data, short=short)
        db.session.add(url)
        db.session.commit()

        success_message = f'{base_url}/{short}'
        flash(success_message, 'success-message')

    return render_template('yacut.html', form=form)


@app.route('/<string:id>')
def redirect_to_source(id):
    short = id
    db_object = URL_map.query.filter_by(short=short).first()
    if db_object is None:
        abort(404)
    source = db_object.original

    return redirect(source)