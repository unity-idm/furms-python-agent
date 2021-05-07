# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
import os
import time
from pathlib import Path
from tinydb import TinyDB, Query
from furms import Header


class ProjectsManagementHandler:
    """
    Simplistic projects management: all projects are accepted except of those with bomb and nuke in name.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.db = TinyDB('projects.json')

    def handle_project_add(self, request: furms.ProjectInstallationRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:

        if "bomb" in request.name:
            sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.ProjectInstallationRequestAck())
            time.sleep(5)
            sitePublisher.publish(Header.error(header.messageCorrelationId, "security_validation", "Creating bombs is prohibited"), 
                                  furms.ProjectInstallationResult())
            return
            
        if "nuke" in request.name:
            headerFailResponse = Header.error(header.messageCorrelationId, "security_validation",
                                              "Creating nuclear bombs is completely prohibited")
            sitePublisher.publish(headerFailResponse, furms.ProjectInstallationRequestAck())
            return

        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.ProjectInstallationRequestAck())
        time.sleep(10)
        self.db.insert({'id': request.identifier, 'name': request.name, 'researchField': request.researchField})
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.ProjectInstallationResult())
        self._logger.info("Project added, list of all projects: %s" % self.db.all())

    def handle_project_remove(self, request: furms.ProjectRemovalRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        Project = Query()
        if not self.db.contains(Project.id == request.identifier):
            headerResponse = Header.error(header.messageCorrelationId, "unknown_project", "Project not found")
            sitePublisher.publish(headerResponse, furms.ProjectRemovalResult())
            return
        
        self.db.remove(Project.id == request.identifier)
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.ProjectRemovalResult())
        self._logger.info("Project removed, list of all projects: %s" % self.db.all())

    def handle_project_update(self, request: furms.ProjectUpdateRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        Project = Query()
        if not self.db.contains(Project.id == request.identifier):
            headerResponse = Header.error(header.messageCorrelationId, "unknown_project", "Project not found")
            sitePublisher.publish(headerResponse, furms.ProjectRemovalResult())
            return
        
        self.db.update({'name' : request.name, 'researchField' : request.researchField}, Project.id == request.identifier)
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.ProjectUpdateResult())
        self._logger.info("Project updated, list of all projects: %s" % self.db.all())