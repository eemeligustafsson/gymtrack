from extensions import db
from alembic import op

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String(200), nullable=False, unique=True)

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @staticmethod
    def create(title, content):
        new_program = Exercise(title, content)
        db.session.add(new_program)
        db.session.commit()