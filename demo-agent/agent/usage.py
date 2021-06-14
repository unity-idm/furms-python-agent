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

class ResourceUsagePublisher:
    def __init__(self, args) -> None:
        self.siteid = args.site
        self.record = self._create_usage_record(args.fenix_user_id, args.allocation_id, args.cumulative_consumption)

    def publish_to_furms(self):
        publisher = furms.SimpleSitePublisher(DemoBrokerConfiguration(self.siteid))
        header = furms.Header.ok(None)
        publisher.publish(header, self.record)

    def _create_usage_record(self, fenix_user_id, allocation_id, cumulative_consumption):
        if fenix_user_id:
            return self._create_user_resource_usage_record(fenix_user_id, allocation_id, cumulative_consumption)
        else:
            return self._create_cumulative_resource_usage_record(allocation_id, cumulative_consumption)

    def _create_user_resource_usage_record(self, fenix_user_id, allocation_id, cumulative_consumption):
        alloc = self._get_allocation(allocation_id)
        return furms.UserResourceUsageRecord(
            alloc['projectIdentifier'], 
            alloc['allocationIdentifier'], 
            fenix_user_id, 
            cumulative_consumption, 
            self._utcnow())

    def _create_cumulative_resource_usage_record(self, allocation_id, cumulative_consumption):
        alloc = self._get_allocation(allocation_id)
        return furms.CumulativeResourceUsageRecord(
            alloc['projectIdentifier'], 
            alloc['allocationIdentifier'], 
            cumulative_consumption, 
            self._utcnow())

    def _get_allocation(self, allocation_id):
        storage = Storage(self.siteid)
        Allocation = Query()
        alloc = storage.allocationsDB.search(Allocation.allocationIdentifier == allocation_id)
        if len(alloc) == 0:
            raise Exception("Unknown allocation identifier %s for site %s" % (allocation_id, self.siteid))
        return alloc[0]

    def _utcnow(self):
        return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def publish_usage_to_furms(args):
    publisher = ResourceUsagePublisher(args)
    publisher.publish_to_furms()

def list_all_allocations(args):
    storage = Storage(args.site)
    allocs = storage.allocationsDB.all()
    print("List of all allocations for site with identifier: %s" % args.site)
    print(json.dumps(allocs, indent=4))

def parse_arguments():
    parser = argparse.ArgumentParser(prog='report-usage.sh', description='Tool to reports usage of records to FURMS.')
    parser.add_argument('-s', '--site', metavar='siteId', help="site's identifier", action='store', required=True)
    subparsers = parser.add_subparsers(title='commands', description='available commands', dest='cmd', required=True)
    
    publish_usage = subparsers.add_parser('publish-usage', aliases=['pub'], help='publish usage of records to FURMS')
    publish_usage.add_argument('-c', '--cumulative-consumption', type=float, help='value how much of an allocation should be reported \
        as consumed', required=True)
    publish_usage.add_argument('-a', '--allocation-id', type=str, help='allocation id', required=True)
    publish_usage.add_argument('-u', '--fenix-user-id', type=str, help='if provided then per-user record is sent together \
        with cumulative allocation data', required=False)
    publish_usage.set_defaults(func=publish_usage_to_furms)

    list_allocs = subparsers.add_parser('list-allocations', aliases=['list'], help='list of site allocations')
    list_allocs.set_defaults(func=list_all_allocations)

    return parser.parse_args()

def main():
    furms.set_stream_logger('furms.sitelistener', logging.DEBUG)
    args = parse_arguments()
    args.func(args)

main()