import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))) )
from app import app, db
from models.project import Project
from models.category import Category

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Projects' in response.data

def test_add_project(client):
    # Add a category first
    with app.app_context():
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()
        category_id = category.id
    response = client.post('/add', data={
        'name': 'Test Project',
        'description': 'A test project',
        'category_id': category_id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Project' in response.data

def test_edit_project(client):
    with app.app_context():
        category = Category(name='EditCat')
        db.session.add(category)
        db.session.commit()
        category_id = category.id
        project = Project(name='EditMe', description='desc', category_id=category_id)
        db.session.add(project)
        db.session.commit()
        pid = project.id
    # Only use category_id outside app context
    response = client.post(f'/edit/{pid}', data={
        'name': 'Edited',
        'description': 'new desc',
        'category_id': category_id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Edited' in response.data

def test_delete_project(client):
    with app.app_context():
        category = Category(name='DelCat')
        db.session.add(category)
        db.session.commit()
        project = Project(name='DeleteMe', description='desc', category_id=category.id)
        db.session.add(project)
        db.session.commit()
        pid = project.id
    response = client.get(f'/delete/{pid}', follow_redirects=True)
    assert response.status_code == 200
    assert b'DeleteMe' not in response.data

def test_project_detail_404(client):
    response = client.get('/projects/9999')
    assert response.status_code == 404

def test_category_detail_404(client):
    response = client.get('/categories/9999')
    assert response.status_code == 404
