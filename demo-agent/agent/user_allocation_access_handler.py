# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
from storage import Storage
from furms import Header, UserAllocationGrantAccessResult
from tinydb import Query


class UserAllocationAccessHandler:
    """
    Simplistic user allocation access management: all grants are accepted except of users whose name contains ‘junior’ string
    and their allocation size is >= 1000
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, storage: Storage) -> None:
        self.db = storage.usersAccessDB
        self.usersDB = storage.usersDB
        self.allocationsDB = storage.allocationsDB

    def handle_add_user_allocation_access(self, request: furms.UserAllocationGrantAccessRequest, header: furms.Header,
                                          sitePublisher: furms.SitePublisher) -> None:
        User = Query()
        user = self.usersDB.search(User.fenixIdentifier == request.user['fenixUserId'])
        Allocation = Query()
        alloc = self.allocationsDB.search(Allocation.allocationIdentifier == request.allocationIdentifier)

        if len(user) == 0:
            sitePublisher.publish(Header.error(header.messageCorrelationId, "allocation_user_not_found",
                                               "Protocol consistency problem: user not installed"), UserAllocationGrantAccessResult())
            return
        if len(alloc) == 0:
            sitePublisher.publish(Header.error(header.messageCorrelationId, "allocation_not_found",
                                               "Protocol consistency problem: allocation not installed"), UserAllocationGrantAccessResult())
            return

        if "junior" in user[0]['name'] and alloc[0]['amount'] > 200:
            sitePublisher.publish(Header.error(header.messageCorrelationId, "allocation__too_big",
                                               "Juniors can't use that big resources"), UserAllocationGrantAccessResult())
            return

        self.db.insert({
            'allocationIdentifier': request.allocationIdentifier,
            'projectIdentifier': request.projectIdentifier,
            'fenixUserId': request.user['fenixUserId']
        })
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.UserAllocationGrantAccessResult())
        self._logger.info("Resource access added, all allocation grants: %s" % self.db.all())

    def handle_remove_user_allocation_access(self, request: furms.UserAllocationBlockAccessRequest, header: furms.Header,
                                             sitePublisher: furms.SitePublisher) -> None:
        AccessGrant = Query()
        if not self.db.contains((AccessGrant.fenixUserId == request.fenixUserId)
                                & (AccessGrant.projectIdentifier == request.projectIdentifier)
                                & (AccessGrant.allocationIdentifier == request.allocationIdentifier)):
            sitePublisher.publish(Header.error(header.messageCorrelationId, "unknown_access_grant", "Access grant not found"),
                                  furms.UserAllocationBlockAccessResult())
        else:
            self.db.remove((AccessGrant.fenixUserId == request.fenixUserId)
                                & (AccessGrant.projectIdentifier == request.projectIdentifier)
                                & (AccessGrant.allocationIdentifier == request.allocationIdentifier))
            sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.UserAllocationBlockAccessResult())
            self._logger.info("User access grant to allocation removed, all grants: %s" % self.db.all())
