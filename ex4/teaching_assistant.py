import json

import pika


class TeachingAssistant:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="validation_queue")
        self.channel.queue_bind(
            exchange="assignment_exchange",
            queue="validation_queue",
            routing_key="validation_queue"
        )
        self.channel.basic_consume(queue="validation_queue", on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        assignment = json.loads(body)
        print(f"Teaching Assistant: Received assignment - {assignment}")
        print()
        assignment["status"] = "validated"
        self.channel.basic_publish(
            exchange="assignment_exchange",
            routing_key="result_queue",
            body=json.dumps(assignment).encode("utf-8")
        )

    def start_consuming(self):
        print("TA: Start consuming messages...")
        self.channel.start_consuming()


TeachingAssistant()
