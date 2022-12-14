from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.session import Session
from models.user import User
from schemas.session import SessionSchema

session_schema = SessionSchema()
session_list_schema = SessionSchema(many=True)


class SessionListResource(Resource):
    @jwt_required(optional=False)
    def get(self):
        current_user = get_jwt_identity()
        user = User.get_by_id(current_user)

        sessions = Session.get_all_by_user(user_id=user.id, visibility='private')
        return session_list_schema.dump(sessions), HTTPStatus.OK

    @jwt_required(optional=False)
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()

        user = User.get_by_id(current_user)
        #data, errors = recipe_schema.load(data=json_data)
        data = session_schema.load(data=json_data)
        #if errors:
            #return {'message': "validation errors", 'error': errors}, HTTPStatus.BAD_REQUEST


        user.session_count += 1
        user.save()
        session = Session(**data)
        session.user_id = current_user

        session.save()

        return session_schema.dump(session), HTTPStatus.CREATED


class SessionResource(Resource):

    @jwt_required(optional=False)
    def get(self, session_id):

        session = Session.get_by_id(session_id=session_id)

        if session is None:
            return {'message': 'Session with such id not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if session.is_publish == False and session.user_id != current_user:
            return {'message': 'Access to view this session is not allowed'}, HTTPStatus.FORBIDDEN

        return session_schema.dump(session), HTTPStatus.OK


    @jwt_required(optional=False)
    def patch(self, session_id):
        json_data = request.get_json()

        #data, errors = recipe_schema.load(data=json_data, partial=('name',))
        data = session_schema.load(data=json_data, partial=('name',))

        #if errors:
            #return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
        session = Session.get_by_id(session_id=session_id)
        if session is None:
            return {'message': 'Session with such id not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != session.user_id:
            return {'message': 'Access to this session is not allowed'}, HTTPStatus.FORBIDDEN

        session.description = data.get('description') or session.description
        session.length = data.get('length') or session.length
        session.walking_distance = data.get('walking_distance') or session.walking_distance
        session.running_distance = data.get('running_distance') or session.running_distance
        session.steps = data.get('steps') or session.steps
        session.other_exercises = data.get('other_exercises') or session.other_exercises
        session.bodyweight = data.get('bodyweight') or session.bodyweight

        session.save()
        return session_schema.dump(session), HTTPStatus.OK

    @jwt_required(optional=False)
    def delete(self, session_id):

        session = Session.get_by_id(session_id=session_id)

        if session is None:
            return {'message': 'Session with such id not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != session.user_id:
            return {'message': 'Access to this session is not allowed'}, HTTPStatus.FORBIDDEN

        session.delete()

        return {}, HTTPStatus.NO_CONTENT


class SessionPublishResource(Resource):

    @jwt_required(optional=False)

    def put(self, session_id):
        session = Session.get_by_id(session_id=session_id)
        if session is None:
            return {'message': 'session wit such id not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != session.user_id:
            return {'message': 'Access to this session is not allowed'}, HTTPStatus.FORBIDDEN

        session.is_publish = True
        session.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required(optional=False)
    def delete(self, session_id):
        session = Session.get_by_id(session_id=session_id)

        if session is None:
            return {'message': 'session with such id not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != session.user_id:
            return {'message': 'Access to this session is not allowed'}, HTTPStatus.FORBIDDEN

        session.is_publish = False
        session.save()

        return {}, HTTPStatus.NO_CONTENT