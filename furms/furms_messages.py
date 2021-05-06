# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

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
class UserSSHKeyAddRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyAddRequest(ProtocolMessage):
    def __init__(self, fenixUserId, publicKey) -> None:
        self.fenixUserId = fenixUserId
        self.publicKey = publicKey

class UserSSHKeyAddResult(ProtocolMessage):
    def __init__(self) -> None:
        pass
    
class UserSSHKeyRemovalRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyRemovalRequest(ProtocolMessage):
    def __init__(self, fenixUserId, publicKey) -> None:
        self.fenixUserId = fenixUserId
        self.publicKey = publicKey

class UserSSHKeyRemovalResult(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyUpdateRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class UserSSHKeyUpdateRequest(ProtocolMessage):
    def __init__(self, fenixUserId, oldPublicKey, newPublicKey) -> None:
        self.fenixUserId = fenixUserId
        self.oldPublicKey = oldPublicKey
        self.newPublicKey = newPublicKey

class UserSSHKeyUpdateResult(ProtocolMessage):
    def __init__(self) -> None:
        pass

###################################################
# Project provisioning messages
###################################################
class ProjectInstallationRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectInstallationRequest(ProtocolMessage):
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

class ProjectInstallationResult(ProtocolMessage):
    def __init__(self) -> None:
        pass
    
class ProjectRemovalRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectRemovalRequest(ProtocolMessage):
    def __init__(self, identifier) -> None:
        self.identifier = identifier

class ProjectRemovalResult(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectUpdateRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectUpdateRequest(ProtocolMessage):
    def __init__(self, identifier, name, description, researchField, validityStart, validityEnd, projectLeader) -> None:
        self.identifier = identifier
        self.name = name
        self.description = description
        self.researchField = researchField
        self.validityStart = validityStart
        self.validityEnd = validityEnd
        self.projectLeader = projectLeader

class ProjectUpdateResult(ProtocolMessage):
    def __init__(self) -> None:
        pass


###################################################
# Project allocation provisioning messages
###################################################
class ProjectResourceAllocationRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectResourceAllocationRequest(ProtocolMessage):
    def __init__(self, projectIdentifier, allocationIdentifier, resourceCreditIdentifier, resourceType, amount,
                 validFrom, validTo) -> None:
        self.projectIdentifier = projectIdentifier
        self.allocationIdentifier = allocationIdentifier
        self.resourceCreditIdentifier = resourceCreditIdentifier
        self.resourceType = resourceType
        self.amount = amount
        self.validFrom = validFrom
        self.validTo = validTo

class ProjectResourceAllocationResult(ProtocolMessage):
    def __init__(self, allocationIdentifier, allocationChunkIdentifier, amount, validFrom, validTo) -> None:
        self.allocationIdentifier = allocationIdentifier
        self.allocationChunkIdentifier = allocationChunkIdentifier
        self.amount = amount
        self.validFrom = validFrom
        self.validTo = validTo
    
class ProjectResourceDeallocationRequestAck(ProtocolMessage):
    def __init__(self) -> None:
        pass

class ProjectResourceDeallocationRequest(ProtocolMessage):
    def __init__(self, projectIdentifier, allocationIdentifier, resourceCreditIdentifier, resourceType) -> None:
        self.projectIdentifier = projectIdentifier
        self.allocationIdentifier = allocationIdentifier
        self.resourceCreditIdentifier = resourceCreditIdentifier
        self.resourceType = resourceType


###################################################
# Ping messages
###################################################
class AgentPingRequest(ProtocolMessage):
    def __init__(self) -> None:
        pass

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

