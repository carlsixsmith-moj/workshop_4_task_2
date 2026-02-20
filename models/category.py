from .project import db

class Category(db.Model):
    """Represents a category for organising projects"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relationship: a category has many projects
    # The 'backref' creates a .category attribute on Project objects
    projects = db.relationship('Project', backref='category', lazy=True)

    def __rep__(self):
        return f"<Category {self.id}: '{self.name}'>"