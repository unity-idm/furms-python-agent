# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import furms
import time

class PingHandler:
    def handle(self, request:furms.AgentPingRequest, header:furms.Header, sitePublisher:furms.SitePublisher):
        time.sleep(1)
        headerResponse = furms.Header(header.messageCorrelationId, header.version, "OK")
        sitePublisher.publish(headerResponse, furms.AgentPingAck())



