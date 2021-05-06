# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import logging
import sys
import os
import time
import furms
from sshkey_handler import SSHKeyRequestHandler
from project_handler import ProjectsManagementHandler
from allocation_handler import ResourceAllocationHandler
from ping_handler import PingHandler

furms.set_stream_logger('furms.sitelistener', logging.DEBUG)
furms.set_stream_logger('sshkey_handler', logging.INFO)
furms.set_stream_logger('project_handler', logging.INFO)
furms.set_stream_logger('allocation_handler', logging.INFO)

#########################################################
# Entry point
#########################################################
if len(sys.argv) != 2:
    print("Provide Site Id as command line parameter.")
    sys.exit(1)

host = os.getenv('BROKER_HOST', '127.0.0.1')
brokerConfig = furms.BrokerConfiguration(
    host=os.getenv('BROKER_HOST', '127.0.0.1'), 
    port=os.getenv('BROKER_PORT', '44444'), 
    username=os.getenv('BROKER_USERNAME', 'guest'), 
    password=os.getenv('BROKER_PASSWORD', 'guest'), 
    cafile=os.getenv('CA_FILE', 'ca_certificate.pem'),
    siteid=sys.argv[1])

listeners = furms.RequestListeners()

ping_handler = PingHandler()
listeners.ping_listener(ping_handler.handle)

ssh_handler = SSHKeyRequestHandler()
listeners.sshkey_add_listener(ssh_handler.handle_sshkey_add)
listeners.sshkey_remove_listener(ssh_handler.handle_sshkey_remove)
listeners.sshkey_update_listener(ssh_handler.handle_sshkey_update)

project_handler = ProjectsManagementHandler()
listeners.project_add_listener(project_handler.handle_project_add)
listeners.project_remove_listener(project_handler.handle_project_remove)
listeners.project_update_listener(project_handler.handle_project_update)

allocation_handler = ResourceAllocationHandler()
listeners.allocation_add_listener(allocation_handler.handle_allocation_add)
listeners.allocation_remove_listener(allocation_handler.handle_allocation_remove)

try:
    furms.SiteListener(config=brokerConfig, listeners=listeners).start_consuming()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
