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

    def handle_project_add(self, request:furms.ProjectInstallationRequest) -> furms.ProjectInstallationResult:
        self._logger.info("Project add request: %s" % request)


        return furms.ProjectInstallationResult()

    def handle_project_remove(self, request:furms.ProjectRemovalRequest) -> furms.ProjectRemovalResult:
        self._logger.info("Project removal request: %s" % request)


        return furms.ProjectRemovalResult()

    def handle_project_update(self, request:furms.ProjectUpdateRequest) -> furms.ProjectUpdateResult:
        self._logger.info("Project update request: %s" % request)


        return furms.ProjectUpdateResult()


