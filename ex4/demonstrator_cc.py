import json

import pika


class CloudComputingDemonstrator:
    def __init__(self):
        print("D_CC_1")
        self.module = "cloud_computing"
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=f"{self.module}_queue")
        self.channel.queue_bind(
            exchange="assignment_exchange",
            queue=f"{self.module}_queue",
            routing_key=f"{self.module}_queue"
        )

        self.channel.basic_consume(queue=f"{self.module}_queue", on_message_callback=self.callback, auto_ack=True)
        self.start_consuming()
        print("D_CC_2")

    def callback(self, ch, method, properties, body):
        assignment = json.loads(body)
        print(f"{self.module.capitalize()} Demonstrator: Received assignment - {assignment}")
        print()
        assignment["status"] = "corrected"
        self.channel.basic_publish(
            exchange="assignment_exchange",
            routing_key="validation_queue",
            body=json.dumps(assignment).encode("utf-8")
        )

    def start_consuming(self):
        print("D_CC_3")

        print("D_CC: Start consuming messages...")
        self.channel.start_consuming()


CloudComputingDemonstrator()
