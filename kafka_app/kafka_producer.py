"""
Kafka Producer module for Django application with SSL support.
This module provides functionality to send messages to Kafka using SSL encryption.
"""

import json
import logging
import os
import ssl
from typing import Dict, Any, Optional

from confluent_kafka import Producer
from django.conf import settings

logger = logging.getLogger(__name__)

class KafkaProducerSSL:
    """
    A Kafka producer that supports SSL encryption for secure communication.
    """

    def __init__(self, bootstrap_servers: str = '192.168.117.128:9093'):
        """
        Initialize the Kafka producer with SSL configuration.

        Args:
            bootstrap_servers: Kafka broker address with port
        """
        self.bootstrap_servers = bootstrap_servers

        # SSL configuration for connecting to Kafka
        # This configuration uses SSL but doesn't verify the certificate
        # which is useful for development environments
        self.config = {
            'bootstrap.servers': self.bootstrap_servers,
            'security.protocol': 'ssl',
            'ssl.endpoint.identification.algorithm': 'none',  # Disable hostname verification
            'client.id': 'django-kafka-ssl-producer',
            'acks': 'all',  # Wait for all replicas to acknowledge
            'retries': 3,   # Retry a few times before giving up
            'retry.backoff.ms': 500,  # Backoff time between retries
        }

        # Create the producer instance
        self.producer = None
        self._create_producer()

    def _create_producer(self):
        """Create the Kafka producer instance with the configured settings."""
        try:
            self.producer = Producer(self.config)
            logger.info(f"Kafka SSL producer created with bootstrap servers: {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to create Kafka SSL producer: {str(e)}")
            raise

    def _delivery_report(self, err, msg):
        """Callback function for message delivery reports."""
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    def send_message(self, topic: str, message: Any, key: Optional[str] = None) -> bool:
        """
        Send a message to the specified Kafka topic.

        Args:
            topic: The Kafka topic to send the message to
            message: The message to send (will be converted to JSON if not a string)
            key: Optional message key

        Returns:
            bool: True if the message was sent successfully, False otherwise
        """
        if not self.producer:
            logger.error("Producer not initialized")
            return False

        try:
            # Convert message to JSON string if it's not already a string
            if not isinstance(message, str):
                message = json.dumps(message)

            # Convert message to bytes
            message_bytes = message.encode('utf-8')
            key_bytes = key.encode('utf-8') if key else None

            # Send the message
            self.producer.produce(
                topic=topic,
                value=message_bytes,
                key=key_bytes,
                callback=self._delivery_report
            )

            # Flush to ensure the message is sent
            self.producer.flush(timeout=10)
            return True

        except Exception as e:
            logger.error(f"Error sending message to Kafka: {str(e)}")
            return False

    def close(self):
        """Close the producer connection."""
        if self.producer:
            self.producer.flush()
            # The confluent_kafka Producer doesn't have a close method
            # It will be garbage collected when it goes out of scope
            self.producer = None
            logger.info("Kafka producer closed")


# Create a singleton instance for the application to use
kafka_ssl_producer = None

def get_kafka_ssl_producer():
    """
    Get or create a singleton instance of the KafkaProducerSSL.

    Returns:
        KafkaProducerSSL: A Kafka producer instance with SSL configuration
    """
    global kafka_ssl_producer
    if kafka_ssl_producer is None:
        kafka_ssl_producer = KafkaProducerSSL()
    return kafka_ssl_producer
