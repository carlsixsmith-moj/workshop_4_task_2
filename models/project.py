from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -- Define the data models
class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'