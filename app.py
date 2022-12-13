from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from models.exercise import Exercise
from config import Config
from extensions import db, jwt


from resources.user import UserListResource, UserResource, MeResource, UserSessionListResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
from resources.session import SessionListResource, SessionResource, SessionPublishResource, SessionAvgLengthResource
from resources.exercise import ExerciseListResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)


    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in black_list


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')

    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(SessionListResource, '/sessions')
    api.add_resource(SessionResource, '/sessions/<int:session_id>')
    api.add_resource(SessionPublishResource, '/sessions/<int:session_id>/publish')

    api.add_resource(SessionAvgLengthResource, '/useraverage/<int:user_id>')

    api.add_resource(UserSessionListResource, '/users/<string:username>/sessions/<string:visibility>')

    api.add_resource(ExerciseListResource, '/exercises')

if __name__ == '__main__':
    app = create_app()
    app.run()