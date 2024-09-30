import pika
import threading
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(override=True)

from src.workers.video_mixer_worker import video_mixer_worker_cb
from src.workers.audio_builder_worker import text_to_audio_worker
from src.workers.image_builder_worker import image_builder_worker

# RabbitMQ connection settings for CloudAMQP
CLOUDAMQP_URL = "amqps://buaalina:6OTVB39Ou0xkMadPjkPNjsukl94w06Tg@armadillo.rmq.cloudamqp.com/buaalina"


class WorkerRegister:
    def __init__(self, amqp_url):
        self.amqp_url = amqp_url
        self.workers = []

    def register(self, queue_name, callback):
        """Register a worker with a specific queue and its callback."""
        worker = threading.Thread(
            target=self._start_worker, args=(queue_name, callback)
        )
        worker.start()
        self.workers.append(worker)

    def _start_worker(self, queue_name, callback):
        """Private method to start the worker for a given queue."""
        params = pika.URLParameters(self.amqp_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declare the queue (it will only be created if it does not exist)
        channel.queue_declare(queue=queue_name, durable=True)

        # Set QoS (fair dispatch)
        channel.basic_qos(prefetch_count=1)

        # Set up the consumer with the provided callback
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=lambda ch, method, properties, body: self._callback_wrapper(
                ch, method, properties, body, callback
            ),
        )

        print(f" [*] Worker started for {queue_name}. Waiting for messages.")

        # Start consuming messages
        channel.start_consuming()

    def _callback_wrapper(self, ch, method, properties, body, callback):
        """A wrapper that executes the user-provided callback and acknowledges the message."""
        callback(ch, method, properties, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def wait_for_completion(self):
        """Wait for all workers to finish."""
        for worker in self.workers:
            worker.join()


if __name__ == "__main__":
    # Create the worker register instance using CloudAMQP connection
    worker_register = WorkerRegister(CLOUDAMQP_URL)

    # Register workers for different queues with their respective callbacks
    worker_register.register("test_queue_0", video_mixer_worker_cb)
    worker_register.register("audio-queue", text_to_audio_worker)
    worker_register.register("image_queue", image_builder_worker)

    # Wait for all threads (workers) to complete
    worker_register.wait_for_completion()
