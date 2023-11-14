from marshmallow import Schema
from marshmallow import fields


class BaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SectorSchema(BaseSchema):
    name = fields.String(required=True)


class RegionSchema(BaseSchema):
    name = fields.String(required=True)


class CountrySchema(BaseSchema):
    name = fields.String(required=True)


class TopicSchema(BaseSchema):
    name = fields.String(required=True)


class SourceSchema(BaseSchema):
    name = fields.String(required=True)


class AnalyticsResponseSchema(BaseSchema):
    title = fields.String(required=True)
    end_year = fields.Integer(allow_none=True)
    start_year = fields.Integer(allow_none=True)
    intensity = fields.Integer(allow_none=True)
    relevance = fields.Integer(allow_none=True)
    likelihood = fields.Integer(allow_none=True)
    insight = fields.String(allow_none=True)
    impact = fields.Integer(allow_none=True)
    url = fields.String(allow_none=True)
    pestle = fields.String(allow_none=True)
    added = fields.DateTime(allow_none=True)
    published = fields.DateTime(allow_none=True)
    source = fields.Nested(SourceSchema, allow_none=True)
    sector = fields.Nested(SectorSchema, allow_none=True)
    country = fields.Nested(CountrySchema, allow_none=True)
    topic = fields.Nested(TopicSchema, allow_none=True)
    region = fields.Nested(RegionSchema, allow_none=True)


class AnalyticsSchema(BaseSchema):
    title = fields.String(required=True)
    end_year = fields.Integer(allow_none=True)
    start_year = fields.Integer(allow_none=True)
    intensity = fields.Integer(allow_none=True)
    relevance = fields.Integer(allow_none=True)
    likelihood = fields.Integer(allow_none=True)
    insight = fields.String(allow_none=True)
    impact = fields.Integer(allow_none=True)
    url = fields.String(allow_none=True)
    pestle = fields.String(allow_none=True)
    added = fields.DateTime(allow_none=True)
    published = fields.DateTime(allow_none=True)
