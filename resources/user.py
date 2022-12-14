from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.session import Session

from schemas.session import SessionSchema

from models.user import User
from schemas.user import UserSchema

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))
session_list_schema = SessionSchema(many=True)


class UserListResource(Resource):
    def post(self):

        json_data = request.get_json()

        # data, errors = user_schema.load(data=json_data)
        data = user_schema.load(data=json_data)

        # if errors:
        # return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_required(optional=True)
    def patch(self, user_id):
        user = User.get_by_id(user_id=user_id)

        json_data = request.get_json()
        data = user_schema.load(data=json_data, partial=('name',))

        if User is None:
            return {'message': 'Session with such id not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != user.user_id:
            return {'message': 'Access to this user is not allowed'}, HTTPStatus.FORBIDDEN

        user.username = data.get('username') or user.username
        user.email = data.get('email') or user.email
        user.password = data.get('password') or user.password
        user.session_count = data.get('session_count') or user.session_count
        user.is_active = data.get('is_active') or user.is_active
        user.save()
        return user_schema.dump(user), HTTPStatus.OK


class MeResource(Resource):

    @jwt_required(optional=False)
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dump(user), HTTPStatus.OK


class UserSessionListResource(Resource):

    @jwt_required(optional=False)
    @use_kwargs({'visibility': fields.Str(missing='private')})
    def get(self, username, visibility):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        print(visibility)
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
        print(visibility)

        sessions = Session.get_all_by_user(user_id=user.id, visibility=visibility)

        return session_list_schema.dump(sessions), HTTPStatus.OK
