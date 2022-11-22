# Copyright (c) 2021 Bixbit s.c. All rights reserved.
# See LICENSE file for licensing information.

import pika
import logging
import ssl
from furms.protocol_messages import Payload
from furms.protocol_messages import Header
from furms.configuration import BrokerConfiguration
from furms.configuration import RequestListeners
from furms.configuration import SitePublisher
from furms.furms_messages import ProtocolMessage

logger = logging.getLogger(__name__)


class SimpleSitePublisher(SitePublisher):
    def __init__(self, config: BrokerConfiguration) -> None:
        self.config = config
        connection = pika.BlockingConnection(self._connection_params())
        self.channel = connection.channel()

    def publish(self, header:Header, message:ProtocolMessage) -> None:
        payload = Payload(header, message)
        response_body = payload.to_body()
        reply_to = self.config.queues.site_to_furms_queue_name()
        self.channel.basic_publish(self.config.exchange, 
            routing_key=reply_to, 
            properties=pika.BasicProperties(
                content_type='application/json', 
                delivery_mode=2, # make message persistent
                content_encoding='UTF-8',
            ),
            body=response_body)
        logger.info("message published to %s (exchange: '%s') payload:\n%s" % (reply_to, self.config.exchange, str(payload)))

    def _connection_params(self) -> pika.ConnectionParameters:
        plain_credentials = pika.credentials.PlainCredentials(self.config.username, self.config.password)
        ssl_options = None
        if self.config.is_ssl_enabled():
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(self.config.cafile)
            ssl_options = pika.SSLOptions(context)

        return pika.ConnectionParameters(
            host=self.config.host, 
            port=self.config.port, 
            credentials=plain_credentials, 
            virtual_host=self.config.virtual_host,
            ssl_options=ssl_options)   


class SiteListener(SimpleSitePublisher):
    def __init__(self, config: BrokerConfiguration, listeners: RequestListeners) -> None:
        SimpleSitePublisher.__init__(self, config)
        self.listeners = listeners

    def start_consuming(self) -> None:
        self.channel.basic_consume(self.config.queues.furms_to_site_queue_name(), self.on_message, auto_ack=True)
        self.channel.start_consuming()    
    
    def on_message(self, channel, basic_deliver, properties, body) -> None:
        logger.debug("Received \nbody=%r\nbasic_deliver=%r, \nproperties=%r" % (body, basic_deliver, properties))

        payload = Payload.from_body(body)
        logger.info("Received payload:\n%s" % str(payload))

        self._handle_request(payload)

    def _handle_request(self, payload:Payload) -> None:
        listener = self.listeners.get(payload.body)
        try:
            listener(payload.body, payload.header, self)
        except Exception as e:
            logger.error("Failed to handle FURMS request: %s", e)



 
