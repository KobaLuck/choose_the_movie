import os
os.environ['DATABASE_URI'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-key'
import pytest
from opinions_app import app, db

@pytest.fixture
def client():
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.mark.parametrize('payload', [[], 'text', 4, True])
def test_non_object_json(client, payload):
    assert client.post('/api/opinions/', json=payload).status_code == 400

@pytest.mark.parametrize('payload', [
    {'title': None, 'text': 'opinion'}, {'title': 'film', 'text': []},
    {'title': 'x' * 129, 'text': 'opinion'}])
def test_invalid_fields(client, payload):
    assert client.post('/api/opinions/', json=payload).status_code == 400

def test_same_text_can_be_saved_on_same_opinion(client):
    response = client.post('/api/opinions/', json={'title':'film','text':'good'})
    assert response.status_code == 201
    pk = response.json['opinion']['id']
    assert client.patch(f'/api/opinions/{pk}/', json={'text':'good'}).status_code < 300

def test_empty_catalog_has_working_home_page(client):
    assert client.get('/').status_code == 200

@pytest.mark.parametrize('payload', [{'text': []}, {'text': {}}, {'text': None}])
def test_invalid_patch_returns_400(client, payload):
    response = client.post('/api/opinions/', json={'title':'film','text':'review'})
    pk = response.json['opinion']['id']
    assert client.patch(f'/api/opinions/{pk}/', json=payload).status_code == 400
