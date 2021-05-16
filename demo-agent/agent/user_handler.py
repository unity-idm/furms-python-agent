# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
from storage import Storage
from furms import Header
from tinydb import TinyDB, Query


class UserInProjectHandler:
    """
    Simplistic users management: all users are accepted except of those with hacker in name.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, storage: Storage) -> None:
        self.db = storage.usersDB
        self.uidNumber = len(self.db)

    def handle_user_add(self, request: furms.UserProjectAddRequest, header: furms.Header, sitePublisher: furms.SitePublisher) -> None:
        User = Query()
        if self.db.contains((User.fenixIdentifier == request.user['fenixUserId']) & (User.project == request.projectIdentifier)):
            sitePublisher.publish(Header.error(header.messageCorrelationId, "duplicate_user", "User already present"),
                                  furms.ProjectRemovalResult())
            return
        # we should also check project's existence

        if "hacker" in request.user['firstName']:
            sitePublisher.publish(Header.error(header.messageCorrelationId, "security_validation", "Hackers should use other sites"),
                                  furms.UserProjectAddRequestAck())
            return

        uid = "user_" + str(self.uidNumber)
        self.db.insert({'fenixIdentifier': request.user['fenixUserId'],
                        'project': request.projectIdentifier,
                        'name': request.user['firstName'],
                        'uid': uid})
        self.uidNumber += 1
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.UserProjectAddResult(uid))
        self._logger.info("User added to project, all users: %s" % self.db.all())

    def handle_user_remove(self, request: furms.UserProjectRemovalRequest, header: furms.Header,
                           sitePublisher: furms.SitePublisher) -> None:
        User = Query()
        if not self.db.contains((User.fenixIdentifier == request.fenixUserId) & (User.project == request.projectIdentifier)):
            sitePublisher.publish(Header.error(header.messageCorrelationId, "unknown_user", "User not found"), furms.ProjectRemovalResult())
        else:
            self.db.remove((User.fenixIdentifier == request.fenixUserId) & (User.project == request.projectIdentifier))
            sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.UserProjectRemovalResult())
            self._logger.info("User removed from project, all users: %s" % self.db.all())
