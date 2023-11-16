import json

import pika


class Demonstrator:
    def __init__(self):
        # Connect to RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        # Declare the correction queue
        self.channel.queue_declare(queue='correction_queue')

        # Bind the correction queue to the assignment exchange
        self.channel.queue_bind(exchange='assignment_exchange', queue='correction_queue')

        # Set up consumer
        self.channel.basic_consume(queue='correction_queue', on_message_callback=self.callback, auto_ack=True)

        # Start consuming messages
        self.start_consuming()

    def callback(self, ch, method, properties, body):
        assignment = json.loads(body)
        print()

        if assignment is not None and assignment['status'] == 'submitted':
            print(f"Demonstrator: Received assignment - {assignment}")
            assignment['status'] = 'corrected'
            self.channel.basic_publish(
                exchange='assignment_exchange',
                routing_key='',
                body=json.dumps(assignment).encode('utf-8')
            )

        elif assignment is not None:
            print(f"D received Assignment with status = {assignment['status']} but ignored it.")

    def start_consuming(self):
        print("D: Start consuming messages...")
        self.channel.start_consuming()


try:
    Demonstrator()
except KeyboardInterrupt:
    print('\nD: Shutdown')
