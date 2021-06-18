# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import logging

from furms.configuration import BrokerConfiguration
from furms.configuration import RequestListeners
from furms.configuration import SitePublisher
from furms.sitelistener import SiteListener
from furms.sitelistener import SimpleSitePublisher

from furms.protocol_messages import Header
from furms.protocol_messages import Error
from furms.protocol_messages import Payload

from furms.furms_messages import AgentPingRequest
from furms.furms_messages import AgentPingAck

from furms.furms_messages import UserSSHKeyAddRequest
from furms.furms_messages import UserSSHKeyAddResult
from furms.furms_messages import UserSSHKeyAddRequestAck

from furms.furms_messages import UserSSHKeyRemovalRequest
from furms.furms_messages import UserSSHKeyRemovalRequestAck
from furms.furms_messages import UserSSHKeyRemovalResult

from furms.furms_messages import UserSSHKeyUpdateRequest
from furms.furms_messages import UserSSHKeyUpdateRequestAck
from furms.furms_messages import UserSSHKeyUpdateResult

from furms.furms_messages import ProjectInstallationRequest
from furms.furms_messages import ProjectInstallationRequestAck
from furms.furms_messages import ProjectInstallationResult

from furms.furms_messages import ProjectRemovalRequest
from furms.furms_messages import ProjectRemovalRequestAck
from furms.furms_messages import ProjectRemovalResult

from furms.furms_messages import ProjectUpdateRequest
from furms.furms_messages import ProjectUpdateRequestAck
from furms.furms_messages import ProjectUpdateResult

from furms.furms_messages import ProjectResourceAllocationRequest
from furms.furms_messages import ProjectResourceAllocationRequestAck
from furms.furms_messages import ProjectResourceAllocationResult
from furms.furms_messages import ProjectResourceAllocationUpdate

from furms.furms_messages import ProjectResourceDeallocationRequest
from furms.furms_messages import ProjectResourceDeallocationRequestAck

from furms.furms_messages import UserProjectAddRequest
from furms.furms_messages import UserProjectAddRequestAck
from furms.furms_messages import UserProjectAddResult

from furms.furms_messages import UserProjectRemovalRequest
from furms.furms_messages import UserProjectRemovalRequestAck
from furms.furms_messages import UserProjectRemovalResult

from furms.furms_messages import UserAllocationGrantAccessRequest
from furms.furms_messages import UserAllocationGrantAccessRequestAck
from furms.furms_messages import UserAllocationGrantAccessResult

from furms.furms_messages import UserAllocationBlockAccessRequest
from furms.furms_messages import UserAllocationBlockAccessRequestAck
from furms.furms_messages import UserAllocationBlockAccessResult

from furms.furms_messages import UserResourceUsageRecord
from furms.furms_messages import CumulativeResourceUsageRecord

__author__ = 'Bixbit s.c.'
__version__ = '1.0.0'


# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger('furms').addHandler(NullHandler())


def set_stream_logger(name='furms', level=logging.DEBUG, format_string=None):
    """
    Add a stream handler for the given name and level to the logging module.
    By default, this logs all messages to ``stdout``.

        >>> import furms
        >>> furms.set_stream_logger('furms.sitelistener', logging.INFO)

    For debugging purposes a good choice is to set the stream logger to ``''``
    which is equivalent to saying "log everything".

    :type name: string
    :param name: Log name
    :type level: int
    :param level: Logging level, e.g. ``logging.INFO``
    :type format_string: str
    :param format_string: Log message format
    """
    if format_string is None:
        format_string = "%(asctime)s %(name)s [%(levelname)s] %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
