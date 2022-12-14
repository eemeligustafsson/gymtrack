from extensions import db

class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.String(1000), nullable=True)
    length = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    walking_distance = db.Column(db.Integer, nullable=True)
    running_distance = db.Column(db.Integer, nullable=True)
    steps = db.Column(db.Integer, nullable=True)
    other_exercises = db.Column(db.String(1000), nullable=True)
    bodyweight = db.Column(db.Integer, nullable=True)
    is_publish = db.Column(db.Boolean(), default=False)
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))


    @classmethod
    def get_by_id(cls, session_id):
        return cls.query.filter_by(id=session_id).first()

    @classmethod
    def get_all_by_user(cls, user_id, visibility):
        if visibility == 'public':
            return cls.query.filter_by(user_id=user_id, is_publish=True).all()

        elif visibility == 'private':
            return cls.query.filter_by(user_id=user_id, is_publish=False).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


