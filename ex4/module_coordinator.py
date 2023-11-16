import json

import pika


class ModuleCoordinator:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='result_queue')
        self.channel.queue_bind(exchange='assignment_exchange', queue='result_queue', routing_key='result_queue')

        self.channel.basic_consume(queue='result_queue', on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        assignment = json.loads(body)
        print(f"Module Coordinator: Received assignment - {assignment}")
        assignment['status'] = 'confirmed'
        print("Module Coordinator: Assignment Confirmed -", assignment)
        print()

    def start_consuming(self):
        print("MC: Start consuming messages...")
        self.channel.start_consuming()


ModuleCoordinator()
