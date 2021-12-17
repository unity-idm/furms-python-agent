# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import os
import furms
import argparse
import json
import datetime
import logging
from demo_broker_config import DemoBrokerConfiguration
from storage import Storage
from tinydb import Query

class ProjectResourceAllocationUpdatePublisher:
    def __init__(self, args) -> None:
        self.siteid = args.site
        self.record = self._create_update(args.allocation_id, args.chunk_id, args.amount, args.valid_from, args.valid_to)

    def update(self):
        publisher = furms.SimpleSitePublisher(DemoBrokerConfiguration(self.siteid))
        header = furms.Header.ok(None)
        Chunk = Query()
        Storage(self.siteid).allocationChunksDB.update({'amount' : self.record.amount, 
            'validFrom' : self.record.validFrom, 'validTo' : self.record.validTo}, 
            (Chunk.allocId == self.record.allocationIdentifier) & (Chunk.chunkId == self.record.allocationChunkIdentifier))
        publisher.publish(header, self.record)

    def _create_update(self, allocation_id, chunk_id, amount, valid_from, valid_to):
        chunk = self._get_chunk(allocation_id, chunk_id)
        return furms.ProjectResourceAllocationUpdate(
            allocation_id, 
            chunk_id, 
            amount, 
            valid_from if valid_from else chunk['validFrom'], 
            valid_to if valid_to else chunk['validTo'])

    def _get_chunk(self, allocation_id, chunk_id):
        storage = Storage(self.siteid)
        Chunk = Query()
        chunk = storage.allocationChunksDB.search((Chunk.allocId == allocation_id) & (Chunk.chunkId == chunk_id))
        if len(chunk) != 1:
            raise Exception("Unknown chunk alloc:%s, chunkId:%s for site %s (result:%s)" % (allocation_id, chunk_id, self.siteid, chunk))
        return chunk[0]

class ProjectResourceAllocationAdder:
    def __init__(self, args) -> None:
        self.siteid = args.site
        self.record = self._create_request(args.allocation_id, args.chunk_id, args.amount, args.valid_from, args.valid_to)

    def add(self):
        publisher = furms.SimpleSitePublisher(DemoBrokerConfiguration(self.siteid))
        header = furms.Header.ok(None)
        Storage(self.siteid).allocationChunksDB.insert(
            {'allocId': self.record.allocationIdentifier,
                        'chunkId': self.record.allocationChunkIdentifier,
                        'amount': self.record.amount,
                        'validFrom': self.record.validFrom,
                        'validTo': self.record.validTo})
        publisher.publish(header, self.record)

    def _create_request(self, allocation_id, chunk_id, amount, valid_from, valid_to):
        return furms.ProjectResourceAllocationResult(
            allocation_id, 
            chunk_id, 
            amount, 
            valid_from, 
            valid_to)



def publish_chunk_update_to_furms(args):
    publisher = ProjectResourceAllocationUpdatePublisher(args)
    publisher.update()


def add_chunk(args):
    publisher = ProjectResourceAllocationAdder(args)
    publisher.add()


def list_all_chunks(args):
    storage = Storage(args.site)
    allocs = storage.allocationChunksDB.all()
    print("List of all chunks for site with identifier: %s" % args.site)
    print(json.dumps(allocs, indent=4))

def parse_arguments():
    parser = argparse.ArgumentParser(prog='chunk-update.sh', description='Tool to publish allocation chunk update to FURMS.')

    required_params = parser.add_argument_group('required arguments')
    required_params.add_argument('-s', '--site', metavar='siteId', help="site's identifier", action='store', required=True)

    subparsers = parser.add_subparsers(title='commands', description='available commands', dest='cmd', required=True)
    
    publish_update = subparsers.add_parser('update-chunk', aliases=['update'], help='update existing chunk')
    publish_update_required = publish_update.add_argument_group('required arguments')
    publish_update_required.add_argument('-a', '--allocation-id', type=str, help='allocation id', required=True)
    publish_update_required.add_argument('-c', '--chunk-id', type=int, help='chunk id', required=True)
    publish_update_required.add_argument('--amount', type=float, help='chunk amount to be updated in FURMS', required=True)

    publish_update.add_argument('-f', '--valid-from', type=str, help='when provided then send in a protocol in validFrom field, \
        if not provided then current provisioned value is taken', required=False)
    publish_update.add_argument('-t', '--valid-to', type=str, help='when provided then send in a protocol in validTo field, , \
        if not provided then current provisioned value is taken', required=False)
    publish_update.set_defaults(func=publish_chunk_update_to_furms)

    add_chunk_opt = subparsers.add_parser('add-chunk', aliases=['add'], help='add new chunk to allocation')
    add_chunk_required = add_chunk_opt.add_argument_group('required arguments')
    add_chunk_required.add_argument('-a', '--allocation-id', type=str, help='allocation id', required=True)
    add_chunk_required.add_argument('-c', '--chunk-id', type=int, help='chunk id', required=True)
    add_chunk_required.add_argument('--amount', type=float, help='chunk amount', required=True)
    add_chunk_required.add_argument('-f', '--valid-from', type=str, help='from when chunk is valid', required=True)
    add_chunk_required.add_argument('-t', '--valid-to', type=str, help='to when chunk is valid', required=True)
    add_chunk_opt.set_defaults(func=add_chunk)

    list_allocs = subparsers.add_parser('list-chunks', aliases=['list'], help='list all chunks')
    list_allocs.set_defaults(func=list_all_chunks)

    return parser.parse_args()

def main():
    furms.set_stream_logger('furms.sitelistener', logging.DEBUG)
    args = parse_arguments()
    args.func(args)

main()