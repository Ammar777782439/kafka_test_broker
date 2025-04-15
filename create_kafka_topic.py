#!/usr/bin/env python
"""
Script to create a Kafka topic.
This script creates a topic in Kafka for testing the Django application.
"""

from confluent_kafka.admin import AdminClient, NewTopic
import sys

def create_topic(bootstrap_servers='localhost:9094', topic_name='test-topic', num_partitions=1, replication_factor=1):
    """
    Create a Kafka topic.
    
    Args:
        bootstrap_servers: Kafka broker address with port (using PLAINTEXT)
        topic_name: Name of the topic to create
        num_partitions: Number of partitions for the topic
        replication_factor: Replication factor for the topic
    """
    # Create admin client
    admin_client = AdminClient({
        'bootstrap.servers': bootstrap_servers
    })
    
    # Create topic
    topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )
    
    # Create the topic on the broker
    try:
        futures = admin_client.create_topics([topic])
        
        # Wait for operation to complete
        for topic_name, future in futures.items():
            future.result()  # Raises exception if creation failed
            print(f"Topic '{topic_name}' created successfully!")
            
    except Exception as e:
        print(f"Failed to create topic: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Get topic name from command line arguments if provided
    topic_name = sys.argv[1] if len(sys.argv) > 1 else 'test-topic'
    create_topic(topic_name=topic_name)
