from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema

def validate_len_in_mins(n):
    if n < 1:
        raise ValidationError('exercise session should be longer than 1 minute.')
    if n > 240:
        raise ValidationError('exercise session should not be longer than 240 minutes.')


class ExerciseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    title = fields.String(validate=[validate.Length(max=1000)])
    content = fields.String(validate=[validate.Length(max=1000)])
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data

    #@validates('')
    #def validate_cook_time(self, value):
        #if value < 1:
            #raise ValidationError('Cook time must be greater than 0.')
        #if value > 300:
            #raise ValidationError('Cook time must not be greater than 300.')