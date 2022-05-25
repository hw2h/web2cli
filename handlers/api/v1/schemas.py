from marshmallow import Schema, fields
from marshmallow.validate import ContainsOnly


class ExecCMDSchema(Schema):
    command = fields.String(required=True)
    arg = fields.String(required=False)
    opts = fields.String(required=False)


class LSSchema(Schema):
    operands = fields.String(required=False)
    options = fields.String(validate=ContainsOnly("-ABCFGHLOPRSTUW@abcdefghiklmnopqrstuwx1%"), required=False)
