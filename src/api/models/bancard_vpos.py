# -*- coding: utf-8 -*-

import hashlib
from marshmallow import fields, Schema, post_dump, post_load

"""
Bancard vpos classes

"""


# Models
class Token(object):
    def __init__(self, private_key, shop_process_id, operation=None, amount=None, currency=None):
        self.private_key = private_key
        self.shop_process_id = str(shop_process_id)
        self.operation = operation
        self.amount = amount
        self.currency = currency

    def __str__(self):
        hash_object = hashlib.md5(self.private_key + self.shop_process_id + (self.operation or '') +
                                  (self.amount or '') + (self.currency or ''))
        return hash_object.hexdigest()


class Operation(object):
    def __init__(self, token, shop_process_id, amount=None, currency=None, additional_data=None, description=None,
                 return_url=None, cancel_url=None, response=None, response_details=None, authorization_number=None,
                 ticket_number=None, response_code=None, response_description=None, extended_response_description=None,
                 security_information=None):

        self.token = str(token)
        self.shop_process_id = shop_process_id
        self.amount = amount
        self.currency = currency
        self.additional_data = additional_data
        self.description = description
        self.return_url = return_url
        self.cancel_url = cancel_url
        self.response = response
        self.response_details = response_details
        self.authorization_number = authorization_number
        self.ticket_number = ticket_number
        self.response_code = response_code
        self.response_description = response_description
        self.extended_response_description = extended_response_description
        self.security_information = security_information


class SecurityInformation(object):
    def __init__(self, customer_ip, version, card_source=None, card_country=None,  risk_index=None):
        self.customer_ip = customer_ip
        self.version = version
        self.card_source = card_source
        self.card_country = card_country
        self.risk_index = risk_index


class Request(object):
    def __init__(self, public_key, operation):
        self.public_key = public_key
        self.operation = operation

    def get_json(self):
        schema = RequestSchema()
        data, errors = schema.dump(self)
        return data or None


class Response(object):
    def __init__(self, status, process_id):
        self.status = status
        self.process_id = process_id


class SingleBuyConfirmRequest(object):
    def __init__(self, operation):
        self.operation = operation


class GetSingleBuyConfirmResponse(object):
    def __init__(self, status, confirmation=None, messages=None):
        self.status = status
        self.confirmation = confirmation
        self.messages = messages


class SingleBuyRollbackResponse(object):
    def __init__(self, status, messages=None):
        self.status = status
        self.messages = messages


class Message(object):
    def __init__(self, key, level, dsc):
        self.key = key
        self.level = level
        self.dsc = dsc


# Schemas
class BaseSchema(Schema):
    SKIP_VALUES = set([None])

    @post_dump
    def remove_skip_values(self, data):
        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
        }


class SecurityInformationSchema(BaseSchema):
    customer_ip = fields.Str()
    version = fields.Str()
    card_source = fields.Str(allow_none=True)
    card_country = fields.Str(allow_none=True)
    risk_index = fields.Int(allow_none=True)

    @post_load
    def make_object(self, data):
        return SecurityInformation(**data)


class OperationSchema(BaseSchema):
    token = fields.Str()
    shop_process_id = fields.Int()
    amount = fields.Str()
    currency = fields.Str()
    additional_data = fields.Str()
    description = fields.Str()
    return_url = fields.Str()
    cancel_url = fields.Str()
    response = fields.Str()
    response_details = fields.Str()
    authorization_number = fields.Str(allow_none=True)
    ticket_number = fields.Str()
    response_code = fields.Str()
    response_description = fields.Str()
    extended_response_description = fields.Str(allow_none=True)
    security_information = fields.Nested(SecurityInformationSchema)

    @post_load
    def make_object(self, data):
        return Operation(**data)


class RequestSchema(Schema):
    public_key = fields.String(required=True)
    operation = fields.Nested(OperationSchema, required=True)


class ResponseSchema(Schema):
    status = fields.Str()
    process_id = fields.Str()

    @post_load
    def make_object(self, data):
        return Response(**data)


class MessageSchema(Schema):
    key = fields.Str()
    level = fields.Str()
    dsc = fields.Str()


class SingleBuyConfirmRequestSchema(Schema):
    operation = fields.Nested(OperationSchema, required=True)

    @post_load
    def make_object(self, data):
        return SingleBuyConfirmRequest(**data)


class GetSingleBuyConfirmResponseSchema(Schema):
    status = fields.Str(required=True)
    confirmation = fields.Nested(OperationSchema)
    messages = fields.Nested(MessageSchema, many=True)

    @post_load
    def make_object(self, data):
        return GetSingleBuyConfirmResponse(**data)


class SingleBuyRollbackResponseSchema(Schema):
    status = fields.Str(required=True)
    messages = fields.Nested(MessageSchema, many=True)

    @post_load
    def make_object(self, data):
        return SingleBuyRollbackResponse(**data)
