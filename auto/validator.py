from marshmallow import Schema, ValidationError, validates, fields


class TestCaseSchema(Schema):
    name = fields.Str(required=True)
    id = fields.Int(required=True)
    function = fields.Str(required=True)
    check_method = fields.Str()
    url = fields.Str(required=True)
    method = fields.Str()
    message = fields.Str()
    parameter = fields.Dict()

    @validates('check_method')
    def validate_check_method(self, value):
        if value and value.upper() not in ['DB', 'MESSAGE']:
            raise ValidationError('check method must in db or message')

    @validates('method')
    def validate_method(self, value):
        if value and value.upper() not in ['POST', 'GET', 'PUT', 'DELETE']:
            raise ValidationError('method must in  put、get、post、delete')


# def main():
#     from auto.operate_file import operate_yaml

#     data = operate_yaml(r'D:\python_code\auto\case\yaml\add_cateory.yaml')
#     schema = TestCaseSchema(data[0].get('id'), r'D:\python_code\auto\case\yaml\add_cateory.yaml')
#     schema = schema.load(data[0])
#     print(schema)
#     print('errors {}'.format(schema.errors))
