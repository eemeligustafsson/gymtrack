from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.session import Session
from schemas.session import SessionSchema

session_schema = SessionSchema()
session_list_schema = SessionSchema(many=True)


class SessionListResource(Resource):

    def get(self):

        sessions = Session.get_all_published()

        return session_list_schema.dump(sessions), HTTPStatus.OK

    @jwt_required(optional=False)
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()

        #data, errors = recipe_schema.load(data=json_data)
        data = session_schema.load(data=json_data)
        #if errors:
            #return {'message': "validation errors", 'error': errors}, HTTPStatus.BAD_REQUEST

        session = Session(**data)
        session.user_id = current_user
        session.save()

        return session_schema.dump(session), HTTPStatus.CREATED


class SessionResource(Resource):

    @jwt_required(optional=True)
    def get(self, session_id):

        session = Session.get_by_id(session_id=session_id)

        if session is None:
            return {'message': 'Session with such id not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if session.is_publish == False and session.user_id != current_user:
            return {'message': 'Access to view this session is not allowed'}, HTTPStatus.FORBIDDEN

        return session.data(), HTTPStatus.OK

    @jwt_required(optional=False)
    def put(self, session_id):

        json_data = request.get_json()

        session = Session.get_by_id(session_id=session_id)

        if session is None:
            return {'message': 'Session with such id not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != session.user_id:
            return {'message': 'Access to view this session is not allowed'}, HTTPStatus.FORBIDDEN

        session.description = json_data['description']
        session.lengthInMinutes = json_data['description']
        session.stepsTaken = json_data['stepsTaken']
        session.pushUps = json_data['pushUps']
        session.pullUps = json_data['pullUps']
        session.otherExercises = json_data['otherExercises']
        session.bodyWeightInKG = json_data['bodyWeightInKG']

        session.save()

        return session.data(), HTTPStatus.OK

    @jwt_required(optional=False)
    def patch(self, recipe_id):
        json_data = request.get_json()

        #data, errors = recipe_schema.load(data=json_data, partial=('name',))
        data = recipe_schema.load(data=json_data, partial=('name',))

        #if errors:
            #return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.name = data.get('name') or recipe.name
        recipe.description = data.get('description') or recipe.description
        recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
        recipe.cook_time = data.get('cook_time') or recipe.cook_time
        recipe.directions = data.get('directions') or recipe.directions

        recipe.save()
        return recipe_schema.dump(recipe), HTTPStatus.OK

    @jwt_required(optional=False)
    def delete(self, recipe_id):

        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.delete()

        return {}, HTTPStatus.NO_CONTENT


class RecipePublishResource(Resource):

    @jwt_required(optional=False)

    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = True
        recipe.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required(optional=False)
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        recipe.is_publish = False
        recipe.save()

        return {}, HTTPStatus.NO_CONTENT