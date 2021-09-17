
# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

from abc import abstractmethod
from typing import Callable
from furms.furms_messages import *
from furms.protocol_messages import Header

"""Abstractions to interact with service models."""


class SitePublisher:
    @abstractmethod
    def publish(self, header:Header, message:ProtocolMessage) -> None: raise NotImplementedError


class Queues:
    """Holds the names of the queues used for communication with FURMS"""
    def __init__(self, siteid):
        self.__site_to_furms = "%s-site-pub" % siteid
        self.__furms_to_site = "%s-furms-pub" % siteid

    def furms_to_site_queue_name(self) -> str:
        return self.__furms_to_site

    def site_to_furms_queue_name(self) -> str:
        return self.__site_to_furms

class BrokerConfiguration:
    """Holds the information required to connect with broker."""
    def __init__(self, siteid, username, password, host, port, exchange=None, virtual_host="/", cafile=None):
        self.queues = Queues(siteid)
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.virtual_host = virtual_host
        self.exchange = exchange if exchange else self.queues.site_to_furms_queue_name()
        """
        The cafile string, if present, is the path to a file of 
        concatenated CA certificates in PEM format.
        """
        self.cafile = cafile

    def is_ssl_enabled(self) -> bool:
        return self.cafile != None


class RequestListeners:
    def __init__(self):
        self.listeners = {}

    def ping_listener(self, listener: Callable[[AgentPingRequest, Header, SitePublisher], None]):
        self.listeners[AgentPingRequest.message_name()] = listener
        return self

    def sshkey_add_listener(self, listener: Callable[[UserSSHKeyAddRequest, Header, SitePublisher], None]):
        self.listeners[UserSSHKeyAddRequest.message_name()] = listener
        return self

    def sshkey_remove_listener(self, listener: Callable[[UserSSHKeyRemovalRequest, Header, SitePublisher], None]):
        self.listeners[UserSSHKeyRemovalRequest.message_name()] = listener
        return self

    def sshkey_update_listener(self, listener: Callable[[UserSSHKeyUpdateRequest, Header, SitePublisher], None]):
        self.listeners[UserSSHKeyUpdateRequest.message_name()] = listener
        return self

    def project_add_listener(self, listener: Callable[[ProjectInstallationRequest, Header, SitePublisher], None]):
        self.listeners[ProjectInstallationRequest.message_name()] = listener
        return self

    def project_remove_listener(self, listener: Callable[[ProjectRemovalRequest, Header, SitePublisher], None]):
        self.listeners[ProjectRemovalRequest.message_name()] = listener
        return self

    def project_update_listener(self, listener: Callable[[ProjectUpdateRequest, Header, SitePublisher], None]):
        self.listeners[ProjectUpdateRequest.message_name()] = listener
        return self

    def allocation_add_listener(self, listener: Callable[[ProjectResourceAllocationRequest, Header, SitePublisher], None]):
        self.listeners[ProjectResourceAllocationRequest.message_name()] = listener
        return self

    def allocation_remove_listener(self, listener: Callable[[ProjectResourceDeallocationRequest, Header, SitePublisher], None]):
        self.listeners[ProjectResourceDeallocationRequest.message_name()] = listener
        return self

    def user_add_listener(self, listener: Callable[[UserProjectAddRequest, Header, SitePublisher], None]):
        self.listeners[UserProjectAddRequest.message_name()] = listener
        return self

    def user_remove_listener(self, listener: Callable[[UserProjectRemovalRequest, Header, SitePublisher], None]):
        self.listeners[UserProjectRemovalRequest.message_name()] = listener
        return self

    def user_add_allocation_access_listener(self, listener: Callable[[UserAllocationGrantAccessRequest, Header, SitePublisher], None]):
        self.listeners[UserAllocationGrantAccessRequest.message_name()] = listener
        return self

    def user_remove_allocation_access_listener(self, listener: Callable[[UserAllocationBlockAccessRequest, Header, SitePublisher], None]):
        self.listeners[UserAllocationBlockAccessRequest.message_name()] = listener
        return self

    def user_policy_acceptance_update_listener(self, listener: Callable[[UserPolicyAcceptanceUpdate, Header, SitePublisher], None]):
        self.listeners[UserPolicyAcceptanceUpdate.message_name()] = listener
        return self

    def policy_update_listener(self, listener: Callable[[PolicyUpdate, Header, SitePublisher], None]):
        self.listeners[PolicyUpdate.message_name()] = listener
        return self

    def get(self, message: ProtocolMessage):
        return self.listeners.get(message.message_name(), lambda: None)
