# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
import os
from pathlib import Path

class ProjectsManagementHandler:
    """
    """
    _logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        pass

    def handle_project_add(self, request:furms.ProjectInstallationRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("Project add request: %s" % request)

        if "bomb" in request.name:
            headerOKResponse = self._header_from(header)
            sitePublisher.publish(headerOKResponse, furms.ProjectInstallationRequestAck())
            
            headerFailResponse = furms.Header(header.messageCorrelationId, 1, "FAILED", 
                            furms.Error("security_validation", "Creating bombs is prohibited"))
            sitePublisher.publish(headerFailResponse, furms.ProjectInstallationResult())
            
        elif "nuke" in request.name:
            headerFailResponse = furms.Header(header.messageCorrelationId, 1, "FAILED", 
                            furms.Error("security_validation", "Creating nuclear bombs is completely prohibited"))
            sitePublisher.publish(headerFailResponse, furms.ProjectInstallationRequestAck())

        else:
            headerResponse = self._header_from(header)
            sitePublisher.publish(headerResponse, furms.ProjectInstallationRequestAck())
            sitePublisher.publish(headerResponse, furms.ProjectInstallationResult())


    def handle_project_remove(self, request:furms.ProjectRemovalRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("Project removal request: %s" % request)

        headerResponse = self._header_from(header)
        sitePublisher.publish(headerResponse, furms.ProjectRemovalRequestAck())

        sitePublisher.publish(headerResponse, furms.ProjectRemovalResult())


    def handle_project_update(self, request:furms.ProjectUpdateRequest, header:furms.Header, sitePublisher:furms.SitePublisher) -> None:
        self._logger.info("Project update request: %s" % request)

        headerResponse = self._header_from(header)
        sitePublisher.publish(headerResponse, furms.ProjectUpdateRequestAck())

        sitePublisher.publish(headerResponse, furms.ProjectUpdateResult())


    def _header_from(self, header:furms.Header):
        return furms.Header(header.messageCorrelationId, header.version, "OK")

