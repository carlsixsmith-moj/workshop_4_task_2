from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -- Define the data models
class Project(db.Model):
    """Represents a software project in the database"""

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    # Foreign key linking to the Category table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'