# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import logging
import datetime
from furms import Header, ProjectResourceAllocationRequestAck, ProjectResourceAllocationResult, ProjectResourceAllocationRequest
from tinydb import TinyDB, Query


class ResourceAllocationHandler:
    """
    Demo resource allocation handling:
    * accepts any resource type
    * if amount <100 then allocates it completely immediately
    * if 100 <= amount < 1000 then allocates it in two equal halves (also dividing allocation period in half)
    * if amount >= 1000 then fails to allocate
    """
    _logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.db = TinyDB('allocations.json')
        self.allocChunkId = len(self.db)

    def handle_allocation_add(self, request: ProjectResourceAllocationRequest, header: Header, sitePublisher: furms.SitePublisher) -> None:
        if request.amount >= 1000:
            sitePublisher.publish(Header.error(header.messageCorrelationId, "allocation_too_large", "We are a demo site..."),
                                  ProjectResourceAllocationRequestAck())
            return

        if request.amount >= 100:
            self._handle_medium_alloc(request, header, sitePublisher)
            return

        self._handle_small_alloc(request, header, sitePublisher)

    def handle_allocation_remove(self, request: furms.ProjectResourceDeallocationRequest, header: Header,
                                 sitePublisher: furms.SitePublisher) -> None:
        self._logger.info("Resource allocation removal request: %s" % request)
        Alloc = Query()
        self.db.remove(Alloc.allocId == request.allocationIdentifier)
        sitePublisher.publish(Header.ok(header.messageCorrelationId), furms.ProjectResourceDeallocationRequestAck())
        self._logger.info("Resource allocation removed, all allocations: %s" % self.db.all())

    def _handle_small_alloc(self, request: ProjectResourceAllocationRequest, header: Header, sitePublisher: furms.SitePublisher):
        sitePublisher.publish(Header.ok(header.messageCorrelationId), ProjectResourceAllocationRequestAck())
        allocResult = ProjectResourceAllocationResult(request.allocationIdentifier, self.allocChunkId,
                                                      request.amount, request.validFrom, request.validTo)
        self._store(allocResult)
        sitePublisher.publish(Header.ok(header.messageCorrelationId), allocResult)

    def _handle_medium_alloc(self, request: ProjectResourceAllocationRequest, header: Header, sitePublisher: furms.SitePublisher):
        sitePublisher.publish(Header.ok(header.messageCorrelationId), ProjectResourceAllocationRequestAck())

        allocStart = datetime.datetime.strptime(request.validFrom, '%Y-%m-%dT%H:%M:%SZ')
        allocEnd = datetime.datetime.strptime(request.validTo, '%Y-%m-%dT%H:%M:%SZ')
        duration = allocEnd - allocStart

        allocHalfTime = allocStart + (duration / 2)
        chunk1 = ProjectResourceAllocationResult(request.allocationIdentifier,
                                                 self.allocChunkId,
                                                 request.amount / 2,
                                                 request.validFrom,
                                                 ResourceAllocationHandler._format_time(allocHalfTime))
        self._store(chunk1)
        sitePublisher.publish(Header.ok(header.messageCorrelationId), chunk1)

        chunk2 = ProjectResourceAllocationResult(request.allocationIdentifier,
                                                 self.allocChunkId,
                                                 request.amount / 2,
                                                 ResourceAllocationHandler._format_time(allocHalfTime),
                                                 request.validTo)
        self._store(chunk2)
        sitePublisher.publish(Header.ok(header.messageCorrelationId), chunk2)

    def _store(self, chunk):
        self.db.insert({'allocId': chunk.allocationIdentifier,
                        'chunkId': chunk.allocationChunkIdentifier,
                        'amount': chunk.amount,
                        'validFrom': chunk.validFrom,
                        'validTo': chunk.validTo})
        self.allocChunkId += 1
        self._logger.info("Resource allocation chunk added, all allocations: %s" % self.db.all())

    @staticmethod
    def _format_time(dateTime):
        return dateTime.strftime('%Y-%m-%dT%H:%M:%SZ')
