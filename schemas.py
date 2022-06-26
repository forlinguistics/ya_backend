from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.validate import Length, OneOf, Range
import pytz
class Item(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    parentId = fields.String(required=False,load_default=None, allow_none=True)
    price = fields.Integer(required=False,load_default=None, allow_none=True)
    type = fields.String(required=True, validate=OneOf(["OFFER", "CATEGORY"]))


class ImportItem(Item):
    @validates_schema
    def validate_price(self, data, **kwargs):
        if data["type"] == "CATEGORY" and not data["price"] is None:
            raise ValidationError("price for category must be None")


class Imports_schema(Schema):
    items = fields.List(fields.Nested(ImportItem), required=True)
    updateDate = fields.DateTime(required=True)


class Get_schema(Item):
    date = fields.Function(lambda obj: obj['date'].astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[0:-3]+'Z',required=True)
    children = fields.List(fields.Nested(lambda: Get_schema()),default=None)

class Stats_schema(Item):
    items = fields.List(fields.Nested(Item), required=False)

class ErrorSchema(Schema):
    code = fields.Integer(required=True)
    message = fields.String(required=True)
