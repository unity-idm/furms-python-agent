# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
import os
import datetime
from pathlib import Path

class ResourceAllocationHandler:
    """
    """
    _logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        pass

    def handle_allocation_add(self, request:furms.ProjectResourceAllocationRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("Resource allocation add request: %s" % request)

        headerResponse = self._header_from(header)
        sitePublisher.publish(headerResponse, furms.ProjectResourceAllocationRequestAck())
        
        sitePublisher.publish(headerResponse, furms.ProjectResourceAllocationResult(request.allocationIdentifier, 7, 
                request.amount / 2, datetime.datetime.utcnow().isoformat('T', 'seconds') + "Z", datetime.datetime.utcnow().isoformat('T', 'seconds') + "Z"))


    def handle_allocation_remove(self, request:furms.ProjectResourceDeallocationRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("Resource allocation removal request: %s" % request)

        headerResponse = self._header_from(header)
        sitePublisher.publish(headerResponse, furms.ProjectResourceDeallocationRequestAck())


    def _header_from(self, header:furms.Header):
        return furms.Header(header.messageCorrelationId, header.version, "OK")

