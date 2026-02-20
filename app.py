import sys
import os

# add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Project

# -- Create the flask application --
app = Flask(__name__)

# -- Configure the database --
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -- intialise the database with the appo --
db.init_app(app)
   
@app.route('/')
def list_projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')

        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('list_projects'))
    
    return render_template('add_project.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)
    
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description', '')
        db.session.commit()

        return redirect(url_for('list_projects'))
    
    return render_template('edit_project.html', project=project)


@app.route('/delete/<int:id>')
def delete_project(id):
    project = db.session.get(Project, id)

    if project is None:
        abort(404)
    
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('list_projects'))

# Initialise the database 

if __name__ == '__main__':
    with app.app_context():
        db.create_all();

    app.run(debug=True)