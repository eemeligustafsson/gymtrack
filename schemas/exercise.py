from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

class ExerciseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    title = fields.String(validate=[validate.Length(max=1000)])
    content = fields.String(validate=[validate.Length(max=1000)])

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data
