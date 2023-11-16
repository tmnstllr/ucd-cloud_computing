import json

import pika


class TeachingAssistant:
    def __init__(self):
        # Connect to RabbitMQ server
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        # Declare the validation queue
        self.channel.queue_declare(queue='validation_queue')

        # Bind the validation queue to the assignment exchange
        self.channel.queue_bind(exchange='assignment_exchange', queue='validation_queue')

        # Set up consumer
        self.channel.basic_consume(queue='validation_queue', on_message_callback=self.callback, auto_ack=True)

        # Start consuming messages
        self.start_consuming()

    def callback(self, ch, method, properties, body):
        assignment = json.loads(body)
        print()

        if assignment is not None and assignment['status'] == 'corrected':
            print(f"Teaching Assistant: Received assignment - {assignment}")
            assignment['status'] = 'validated'
            self.channel.basic_publish(
                exchange='assignment_exchange',
                routing_key='',
                body=json.dumps(assignment).encode('utf-8')
            )

        elif assignment is not None:
            print(f"TA received Assignment with status = {assignment['status']} but ignored it.")

    def start_consuming(self):
        print("TA: Start consuming messages...")
        self.channel.start_consuming()


try:
    TeachingAssistant()
except KeyboardInterrupt:
    print('\nTA: Shutdown')
