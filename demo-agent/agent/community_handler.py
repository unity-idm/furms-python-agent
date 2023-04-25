# Copyright (c) 2023 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
from furms import Header


class CommunityManagementHandler:
    _logger = logging.getLogger(__name__)
    def handle_community_add(self, request: furms.CommunityInstallationRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        self._logger.info("Community installation request")
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.CommunityInstallationRequestAck())

    def handle_community_update(self, request: furms.CommunityUpdateRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        self._logger.info("Community update request")
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.CommunityUpdateRequestAck())

    def handle_community_remove(self, request: furms.CommunityRemovalRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        self._logger.info("Community removal request")
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.CommunityRemovalRequestAck())


