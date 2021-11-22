# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
from furms import Header, SetUserStatusRequestAck, SetUserStatusResult

class UserStatusHandler:
    _logger = logging.getLogger(__name__)

    def handle_user_status_change(self, request: furms.SetUserStatusRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        self._logger.info("User status change received: user=%s, status=%s, reason=%s" % (request.fenixUserId, request.status, request.reason))
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.SetUserStatusRequestAck()) 
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.SetUserStatusResult()) 

