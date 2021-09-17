# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging

class PolicyManagementHandler:
    _logger = logging.getLogger(__name__)

    def handle_policy_update(self, request: furms.PolicyUpdate, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        self._logger.info("Policy update received: name=%s, version=%s" % (request.policyName, request.currentVersion))

    def handle_user_policy_acceptance_update(self, request: furms.UserPolicyAcceptanceUpdate, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        self._logger.info("User policy acceptance update received: acceptance=%s" % request.policiesAcceptance)

