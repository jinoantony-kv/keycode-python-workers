import pika
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the value of CLOUDAMQP_URL from the .env file
CLOUDAMQP_URL = os.getenv("CLOUDAMQP_URL")

def publish_message(queue_name, message):
    """Publish a message directly to a queue by name (using the default exchange)."""
    # Set up the connection parameters using the CloudAMQP URL
    params = pika.URLParameters(CLOUDAMQP_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Declare the queue to ensure it exists (if it's not already created)
    channel.queue_declare(queue=queue_name, durable=True)

    # Publish the message to the default exchange ('') using the queue name as the routing key
    channel.basic_publish(
        exchange='',  # Use the default exchange
        routing_key=queue_name,  # The routing key is the queue name
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )

    print(f" [x] Sent message to queue '{queue_name}': {message}")

    # Close the connection
    connection.close()


# Uncomment for testing publish

# if __name__ == "__main__":
#     # Example usage: publish a message to the queue "test_queue_0"
#     publish_message("SimpleQueue", "Hello, this is a test message directly to the queue!")


