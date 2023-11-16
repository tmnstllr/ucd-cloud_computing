import json

import pika


class ModuleCoordinator:
    def __init__(self):
        # Connect to RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        # Declare the results queue
        self.channel.queue_declare(queue='results_queue')

        # Bind the results queue to the assignment exchange
        self.channel.queue_bind(exchange='assignment_exchange', queue='results_queue')

        # Set up consumer
        self.channel.basic_consume(queue='results_queue', on_message_callback=self.callback, auto_ack=True)

        # Start consuming messages
        self.start_consuming()

    def callback(self, ch, method, properties, body):
        assignment = json.loads(body)
        print()

        if assignment is not None and assignment['status'] == 'validated':
            print(f"Module Coordinator: Received assignment - {assignment}")
            assignment['status'] = 'confirmed'
            print("Module Coordinator: Assignment Confirmed -", assignment)

        elif assignment is not None:
            print(f"MC received Assignment with status = {assignment['status']} but ignored it.")

    def start_consuming(self):
        print("MC: Start consuming messages...")
        self.channel.start_consuming()


try:
    ModuleCoordinator()
except KeyboardInterrupt:
    print('\nMC: Shutdown')
