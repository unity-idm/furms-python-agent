
# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import json
from furms.furms_messages import ProtocolMessageFactory
from furms.furms_messages import ProtocolMessage

"""
Abstraction that provides Payload definition with serialization and deserialization capabilities.
"""

class Header:
    def __init__(self, messageCorrelationId, version, status=None, error=None):
        self.version = version
        self.messageCorrelationId = messageCorrelationId
        self.status = status
        self.error = error

    @classmethod
    def error(cls, messageCorrelationId, errorCode, errorMessage):
        return Header(messageCorrelationId, 1, 'FAILED', Error(errorCode, errorMessage))

    @classmethod
    def ok(cls, messageCorrelationId):
        return Header(messageCorrelationId, 1, 'OK')
    
    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        ret = {}
        ret['version'] = self.version
        ret['messageCorrelationId'] = self.messageCorrelationId
        ret['status'] = self.status
        if self.status == 'FAILED':
            ret['error'] = self.error.to_dict()
        return ret
    
    def __str__(self) -> str:
        return str(self.to_dict())

class Error:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def to_dict(self) -> dict:
        return {
            key:value
            for key, value in self.__dict__.items()
            if value is not None
        }
    def __str__(self) -> str:
        return str(self.to_dict())

class Payload:
    def __init__(self, header:Header, body:ProtocolMessage) -> None:
        self.header = header
        if body == None:
            raise Exception("body must not be empty")
        self.body = body

    @classmethod
    def from_body(cls, message: str):
        data = json.loads(message)
        header = Header.from_json(data["header"])
        request = ProtocolMessageFactory.from_json(data["body"])
        return cls(header, request)

    def to_body(self, indent=0) -> str:
        payload = {}
        payload['header'] = self.header.to_dict()
        payload['body'] = self.body.to_dict()
        return json.dumps(payload, indent=indent)

    def __str__(self) -> str:
        return self.to_body(indent=2)
