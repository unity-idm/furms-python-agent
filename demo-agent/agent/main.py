# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import logging
import sys
import os
import furms
from storage import Storage
from sshkey_handler import SSHKeyRequestHandler
from project_handler import ProjectsManagementHandler
from allocation_handler import ResourceAllocationHandler
from user_handler import UserInProjectHandler
from ping_handler import PingHandler
from user_allocation_access_handler import UserAllocationAccessHandler

furms.set_stream_logger('furms.sitelistener', logging.DEBUG)
furms.set_stream_logger('sshkey_handler', logging.INFO)
furms.set_stream_logger('project_handler', logging.INFO)
furms.set_stream_logger('allocation_handler', logging.INFO)
furms.set_stream_logger('user_allocation_access_handler', logging.INFO)

#########################################################
# Entry point
#########################################################
if len(sys.argv) != 2:
    print("Provide Site Id as command line parameter.")
    sys.exit(1)

host = os.getenv('BROKER_HOST', '127.0.0.1')
siteId = sys.argv[1]
brokerConfig = furms.BrokerConfiguration(
    host=os.getenv('BROKER_HOST', '127.0.0.1'), 
    port=os.getenv('BROKER_PORT', '44444'), 
    username=os.getenv('BROKER_USERNAME', 'guest'), 
    password=os.getenv('BROKER_PASSWORD', 'guest'), 
    virtual_host=os.getenv('BROKER_VIRTUAL_HOST', '/'), 
    cafile=os.getenv('CA_FILE', 'ca_certificate.pem'),
    siteid=siteId)

listeners = furms.RequestListeners()

storage = Storage(siteId)

ping_handler = PingHandler()
listeners.ping_listener(ping_handler.handle)

ssh_handler = SSHKeyRequestHandler(storage)
listeners.sshkey_add_listener(ssh_handler.handle_sshkey_add)
listeners.sshkey_remove_listener(ssh_handler.handle_sshkey_remove)
listeners.sshkey_update_listener(ssh_handler.handle_sshkey_update)

project_handler = ProjectsManagementHandler(storage)
listeners.project_add_listener(project_handler.handle_project_add)
listeners.project_remove_listener(project_handler.handle_project_remove)
listeners.project_update_listener(project_handler.handle_project_update)

allocation_handler = ResourceAllocationHandler(storage)
listeners.allocation_add_listener(allocation_handler.handle_allocation_add)
listeners.allocation_remove_listener(allocation_handler.handle_allocation_remove)

user_handler = UserInProjectHandler(storage)
listeners.user_add_listener(user_handler.handle_user_add)
listeners.user_remove_listener(user_handler.handle_user_remove)

user_access_handler = UserAllocationAccessHandler(storage)
listeners.user_add_allocation_access_listener(user_access_handler.handle_add_user_allocation_access)
listeners.user_remove_allocation_access_listener(user_access_handler.handle_remove_user_allocation_access)



try:
    furms.SiteListener(config=brokerConfig, listeners=listeners).start_consuming()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
