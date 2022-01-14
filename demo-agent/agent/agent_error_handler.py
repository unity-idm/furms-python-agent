# Copyright (c) 2022 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging

class AgentErrorHandler:
    _logger = logging.getLogger(__name__)
    def handle(self, request:furms.AgentMessageErrorInfo, header:furms.Header, sitePublisher:furms.SitePublisher):
        self._logger.info("Error Message received: errorType=%s, description=%s" % (request.errorType, request.description))



