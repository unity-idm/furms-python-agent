# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
import os
import datetime
from pathlib import Path

class UserInProjectHandler:
    """
    """
    _logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        pass

    def handle_user_add(self, request:furms.UserProjectAddRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("User added to project request: %s" % request)

        headerResponse = self._header_from(header)
        sitePublisher.publish(headerResponse, furms.UserProjectAddRequestAck())
        
        sitePublisher.publish(headerResponse, furms.UserProjectAddResult('site_user_X01'))


    def handle_user_remove(self, request:furms.UserProjectRemovalRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("User removal from project request: %s" % request)

        headerResponse = self._header_from(header)
        sitePublisher.publish(headerResponse, furms.UserProjectRemovalRequestAck())

        sitePublisher.publish(headerResponse, furms.UserProjectRemovalResult())


    def _header_from(self, header:furms.Header):
        return furms.Header(header.messageCorrelationId, header.version, "OK")

