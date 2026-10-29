from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import Opinion
from .views import random_opinion


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise InvalidAPIUsage('Тело запроса должно быть объектом JSON')
    validate_opinion(data, partial=True)
    if (
        'text' in data and 
        Opinion.query.filter(Opinion.text == data['text'], Opinion.id != id).first() is not None
    ):
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()  
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    opinions = Opinion.query.all()  
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise InvalidAPIUsage('Тело запроса должно быть объектом JSON')
    validate_opinion(data)
    if Opinion.query.filter_by(text=data['text']).first() is not None:
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    opinion = random_opinion()
    if opinion is not None:
        return jsonify({'opinion': opinion.to_dict()}), 200
    raise InvalidAPIUsage('В базе данных нет мнений', 404)


def validate_opinion(data, partial=False):
    for field in ('title', 'text'):
        if field not in data and partial:
            continue
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    for field, maximum in (('title', 128), ('source', 256), ('added_by', 64)):
        if field in data and data[field] is not None:
            if not isinstance(data[field], str) or len(data[field]) > maximum:
                raise InvalidAPIUsage('Некорректное значение поля ' + field)
