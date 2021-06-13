# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information

import os
import furms

class DemoBrokerConfiguration(furms.BrokerConfiguration):
    def __init__(self, siteid):
        host=os.getenv('BROKER_HOST', '127.0.0.1')
        port=os.getenv('BROKER_PORT', '44444')
        username=os.getenv('BROKER_USERNAME', 'guest')
        password=os.getenv('BROKER_PASSWORD', 'guest')
        virtual_host=os.getenv('BROKER_VIRTUAL_HOST', '/')
        cafile=os.getenv('CA_FILE', os.getcwd() + '/ca_certificate.pem')
        super().__init__(siteid, username, password, host, port, virtual_host=virtual_host, cafile=cafile)

