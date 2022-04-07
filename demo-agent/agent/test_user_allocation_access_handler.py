import unittest
from unittest.mock import MagicMock, call

from furms import Header, UserAllocationGrantAccessRequest, SitePublisher, UserAllocationGrantAccessResult
from furms.furms_messages import ProtocolMessage, ProjectResourceAllocationRequest, UserAllocationBlockAccessRequest, \
    UserAllocationBlockAccessResult
from user_allocation_access_handler import UserAllocationAccessHandler
from storage import Storage


class FakePublisher(SitePublisher):
    def __init__(self):
        self.message = None
        self.header = None

    def publish(self, header: Header, message: ProtocolMessage) -> None:
        self.header = header
        self.message = message


class TestUserAllocationAccess(unittest.TestCase):
    def test_succeed_add_grant(self):
        alloc_access_handler = UserAllocationAccessHandler(self.storage)

        header = Header("id-1", version=1)
        request = UserAllocationGrantAccessRequest("allocId", {"fenixUserId": "userid"}, "projectId")
        publisher = FakePublisher()
        self.storage.usersDB.insert({'fenixIdentifier': "userid",
                        'project': request.projectIdentifier,
                        'name': "Senior",
                        'uid': "123"})
        self.storage.allocationsDB.insert({'allocationIdentifier': request.allocationIdentifier,
            'projectIdentifier': request.projectIdentifier,
            'resourceCreditIdentifier': "credId",
            'amount': 123, 'validFrom': None, 'validTo': None})

        alloc_access_handler.handle_add_user_allocation_access(request, header, publisher)

        self.assertEqual(publisher.header, Header.ok(header.messageCorrelationId))
        self.assertEqual(publisher.message, UserAllocationGrantAccessResult())

    def test_fail_to_add_grant_missing_user(self):
        alloc_access_handler = UserAllocationAccessHandler(self.storage)

        header = Header("id-1", version=1)
        request = UserAllocationGrantAccessRequest("allocId", {"fenixUserId": "userid"}, "projectId")
        publisher = FakePublisher()

        alloc_access_handler.handle_add_user_allocation_access(request, header, publisher)

        self.assertEqual(publisher.header, Header.error(header.messageCorrelationId, "allocation_user_not_found",
                                               "Protocol consistency problem: user not installed"))
        self.assertEqual(publisher.message, UserAllocationGrantAccessResult())

    def test_fail_to_add_grant_missing_allocation(self):
        alloc_access_handler = UserAllocationAccessHandler(self.storage)

        header = Header("id-1", version=1)
        request = UserAllocationGrantAccessRequest("allocId", {"fenixUserId": "userid"}, "projectId")
        publisher = FakePublisher()
        self.storage.usersDB.insert({'fenixIdentifier': "userid",
                        'project': request.projectIdentifier,
                        'name': "Senior",
                        'uid': "123"})

        alloc_access_handler.handle_add_user_allocation_access(request, header, publisher)

        self.assertEqual(publisher.header, Header.error(header.messageCorrelationId, "allocation_not_found",
                                               "Protocol consistency problem: allocation not installed"))
        self.assertEqual(publisher.message, UserAllocationGrantAccessResult())

    def test_succeed_remove_existing_grant(self):
        alloc_access_handler = UserAllocationAccessHandler(self.storage)

        header = Header("id-1", version=1)
        request = UserAllocationBlockAccessRequest("allocId", {"fenixUserId": "userid"}, "projectId")
        publisher = FakePublisher()
        self.storage.usersAccessDB.insert({
            'allocationIdentifier': request.allocationIdentifier,
            'projectIdentifier': request.projectIdentifier,
            'fenixUserId': request.fenixUserId
        })

        alloc_access_handler.handle_remove_user_allocation_access(request, header, publisher)

        self.assertEqual(publisher.header, Header.ok(header.messageCorrelationId))
        self.assertEqual(publisher.message, UserAllocationBlockAccessResult())

    def setUp(self):
        self.storage = Storage('test-q')

    def tearDown(self):
        self.storage.dispose()


if __name__ == '__main__':
    unittest.main()
