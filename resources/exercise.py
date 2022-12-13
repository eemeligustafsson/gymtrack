from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.exercise import Exercise
from models.user import User
from schemas.exercise import ExerciseSchema

exercise_schema = ExerciseSchema()
exercise_list_schema = ExerciseSchema(many=True)

class ExerciseListResource(Resource):

    def get(self):

        exercises = Exercise.get_all()

        return exercise_list_schema.dump(exercises), HTTPStatus.OK

    @jwt_required(optional=False)
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()

        user = User.get_by_id(current_user)
        #data, errors = recipe_schema.load(data=json_data)
        data = exercise_schema.load(data=json_data)
        #if errors:
            #return {'message': "validation errors", 'error': errors}, HTTPStatus.BAD_REQUEST

        exercise = Exercise(**data)
        exercise.user_id = current_user

        exercise.save()

        return exercise_schema.dump(exercise), HTTPStatus.CREATED