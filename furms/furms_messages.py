# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

from abc import abstractmethod

"""Definition of messages exchanged in payload between FURMS and local site."""

class ProtocolMessage:
    """
    Common boilerplate for all protocol messages
    """
    @classmethod
    def message_name(cls):
        return cls.__name__.split('.')[-1]

    def to_dict(self) -> dict:
        message = {}
        message[self.message_name()] = self.__dict__
        return message
        
    def __str__(self) -> str:
        return str(self.to_dict())

class ProtocolRequestMessage(ProtocolMessage):
    @abstractmethod
    def ack_message(self): raise NotImplementedError


class UserRecord:
    """
    Reusable user record. Does not include all defined attributes as their sake is unknown as of now. 
    """
    def __init__(self, fenixUserId, firstName, lastName, email):
        self.fenixUserId = fenixUserId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

###################################################
# SSH keys messages
###################################################
class UserSSHKeyAddAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyAddRequest(ProtocolRequestMessage):
    def __init__(self, fenixUserId, publicKey) -> None:
        self.fenixUserId = fenixUserId
        self.publicKey = publicKey
    def ack_message(self):
        return UserSSHKeyAddAck()

class UserSSHKeyAddResult(ProtocolMessage):
    def __init__(self) -> None:
        pass
    
class UserSSHKeyRemovalAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyRemovalRequest(ProtocolRequestMessage):
    def __init__(self, fenixUserId, publicKey) -> None:
        self.fenixUserId = fenixUserId
        self.publicKey = publicKey
    def ack_message(self):
        return UserSSHKeyRemovalAck()

class UserSSHKeyRemovalResult(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyUpdateAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyUpdatingRequest(ProtocolRequestMessage):
    def __init__(self, fenixUserId, oldPublicKey, newPublicKey) -> None:
        self.fenixUserId = fenixUserId
        self.oldPublicKey = oldPublicKey
        self.newPublicKey = newPublicKey
    def ack_message(self):
        return UserSSHKeyUpdateAck()

class UserSSHKeyUpdateResult(ProtocolMessage):
    def __init__(self) -> None:
        pass

###################################################
# Project provisioning messages
###################################################
class ProjectInstallationRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectInstallationRequest(ProtocolRequestMessage):
    def __init__(self, identifier, name, description, acronym, communityId, community, researchField, validityStart, 
                 validityEnd, projectLeader) -> None:
        self.identifier = identifier
        self.name = name
        self.description = description
        self.acronym = acronym
        self.communityId = communityId
        self.community = community
        self.researchField = researchField
        self.validityStart = validityStart
        self.validityEnd = validityEnd
        self.projectLeader = projectLeader
    def ack_message(self):
        return ProjectInstallationRequestAck()

class ProjectInstallationResult(ProtocolMessage):
    def __init__(self) -> None:
        pass
    
class ProjectRemovalRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectRemovalRequest(ProtocolRequestMessage):
    def __init__(self, identifier) -> None:
        self.identifier = identifier
    def ack_message(self):
        return ProjectRemovalRequestAck()

class ProjectRemovalResult(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectUpdateRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectUpdateRequest(ProtocolRequestMessage):
    def __init__(self, identifier, name, description, researchField, validityStart, validityEnd, projectLeader) -> None:
        self.identifier = identifier
        self.name = name
        self.description = description
        self.researchField = researchField
        self.validityStart = validityStart
        self.validityEnd = validityEnd
        self.projectLeader = projectLeader
    def ack_message(self):
        return ProjectUpdateRequestAck()

class ProjectUpdateResult(ProtocolMessage):
    def __init__(self) -> None:
        pass

###################################################
# Ping messages
###################################################
class AgentPingRequest(ProtocolRequestMessage):
    def __init__(self) -> None:
        pass
    def ack_message(self):
        return AgentPingAck()

class AgentPingAck(ProtocolMessage):
    def __init__(self) -> None:
        pass


class ProtocolMessageFactory:
    """
    Takes the first key from the body, makes the lookup in current module
    for the class, which name is the same as the first key, and create
    instance of this class.
    """
    def from_json(body: dict) -> ProtocolMessage:
        protocol_message_name = next(iter(body))
        protocol_message_name_class = globals()[protocol_message_name]
        return protocol_message_name_class(**body[protocol_message_name])

