import json

import pika

# Establish a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Task 1
# 1- Using Pika's syntax, declare the necessary queues/exchanges and their connections as given in the Behaviour.

# Declare the assignment exchange
channel.exchange_declare(exchange='assignment_exchange', exchange_type='fanout')

# Declare queues
channel.queue_declare(queue='correction_queue')
channel.queue_declare(queue='validation_queue')
channel.queue_declare(queue='results_queue')

# Bind queues to the exchange
channel.queue_bind(exchange='assignment_exchange', queue='correction_queue')
channel.queue_bind(exchange='assignment_exchange', queue='validation_queue')
channel.queue_bind(exchange='assignment_exchange', queue='results_queue')


# Task 2
# 2- Using Pika's syntax, declare where a demonstrator should listen/subscribe
def demonstrator_callback(ch, method, properties, body):
    assignment = json.loads(body)

    if assignment is not None and assignment['status'] == 'submitted':
        assignment['status'] = 'corrected'
        channel.basic_publish(
            exchange='assignment_exchange',
            routing_key='',
            body=json.dumps(assignment).encode('utf-8')
        )


channel.basic_consume(queue='correction_queue', on_message_callback=demonstrator_callback, auto_ack=True)


# 3- Using Pika's syntax, declare where a TA should listen/subscribe
def ta_callback(ch, method, properties, body):
    assignment = json.loads(body)

    if assignment is not None and assignment['status'] == 'corrected':
        assignment['status'] = 'validated'
        channel.basic_publish(
            exchange='assignment_exchange',
            routing_key='',
            body=json.dumps(assignment).encode('utf-8')
        )


channel.basic_consume(queue='validation_queue', on_message_callback=ta_callback, auto_ack=True)


# 4- Using Pika's syntax, declare where the module coordinator should listen/subscribe
def mc_callback(ch, method, properties, body):
    assignment = json.loads(body)

    if assignment is not None and assignment['status'] == 'validated':
        assignment['status'] = 'confirmed'

        # Log confirmed assigment
        print("Assignment confirmed:", assignment)


channel.basic_consume(queue='results_queue', on_message_callback=mc_callback, auto_ack=True)
