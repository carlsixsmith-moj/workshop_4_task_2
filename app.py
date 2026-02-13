from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# -- Create the flask application --
app = Flask(__name__)

# -- Configure the database --
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -- Connect SQLAlchemy to the app --
db = SQLAlchemy(app)


# -- Define the data models
class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'
    
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
        return 'Project not found', 404
    
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
        return 'Project not found', 404
    
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('list_projects'))

# Initialise the database 

if __name__ == '__main__':
    with app.app_context():
        db.create_all();

    app.run(debug=True)