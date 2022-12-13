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
    #workouts = db.relationship('Exercise', backref='session')
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all_published(cls):
        return cls.query.filter_by(is_publish=True).all()

    @classmethod
    def get_by_id(cls, session_id):
        return cls.query.filter_by(id=session_id).first()

    @classmethod
    def get_avg_length_by_user(cls, user_id,  visibility='public'):
        if visibility == 'public':
            sessions = cls.query.filter_by(user_id=user_id, is_publish=False).all()#sessions by user
            #lengths = sessions.query().with_entities(sessions.length) #lenghts by user
            #average = db.func.round(db.func.avg(sessions['length']), 2)
            #return cls.query.filter_by(user_id=user_id, is_publish=True).all()

            return sessions

        elif visibility == 'private':
            #return cls.query.filter_by(user_id=user_id, is_publish=False).all()
            sessions = cls.query.filter_by(user_id=user_id, is_publish=True).all()  # sessions by user
            # lengths = sessions.query().with_entities(sessions.length) #lenghts by user
            average = db.func.round(db.func.avg(sessions['length']), 2)
            # return cls.query.filter_by(user_id=user_id, is_publish=True).all()
            return average

        else:
            #return cls.query.filter_by(user_id=user_id).all()
            sessions = cls.query.filter_by(user_id=user_id, is_publish=True).all()  # sessions by user
            # lengths = sessions.query().with_entities(sessions.length) #lenghts by user
            average = db.func.round(db.func.avg(sessions['length']), 2)
            # return cls.query.filter_by(user_id=user_id, is_publish=True).all()
            return average


    @classmethod
    def get_all_by_user(cls, user_id, visibility):
        if visibility == 'public':
            return cls.query.filter_by(user_id=user_id, is_publish=True).all()

        elif visibility == 'private':
            return cls.query.filter_by(user_id=user_id, is_publish=False).all()

        else:
            return cls.query.filter_by(user_id=user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


