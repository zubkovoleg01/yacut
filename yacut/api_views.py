from flask import jsonify, request
from . import app, db
from .models import URL_map
from .views import get_random_string
from urllib.parse import urljoin

import re
from http import HTTPStatus

@app.route('/api/id/<string:id>/', methods=['GET'])
def get_original_link(id):
    db_object = URL_map.query.filter_by(short=id).first_or_404()
    return jsonify({'url': db_object.original}), HTTPStatus.OK

@app.route('/api/id/', methods=['POST'])
def get_short_link():
    base_url = request.url_root
    data = request.get_json()

    custom_id = data.get('custom_id')
    if custom_id and re.match(r'^[a-zA-Z0-9]+$', custom_id) and len(custom_id) <= 16:
        short = custom_id
    else:
        short = get_random_string()

    url = URL_map(original=data['url'], short=short)
    db.session.add(url)
    db.session.commit()

    return jsonify({'short_link': urljoin(base_url, short), 'url': data['url']}), HTTPStatus.CREATED
