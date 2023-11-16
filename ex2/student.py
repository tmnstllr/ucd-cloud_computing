import json

import pika


class Student:
    def __init__(self, student_id):
        self.student_id = student_id
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='assignment_exchange', exchange_type='fanout')

    def submit_assignment(self, answer):
        assignment = {'student_id': self.student_id, 'answer': answer, 'status': 'submitted'}
        self.channel.basic_publish(
            exchange='assignment_exchange',
            routing_key='',
            body=json.dumps(assignment).encode('utf-8')
        )
        print(f"Student {self.student_id}: Assignment Submitted")

    def close_connection(self):
        print(f"Student {self.student_id}: Connection closed")
        self.channel.stop_consuming()
        self.connection.close()


student = Student(student_id="123")
student.submit_assignment(answer="Some answer")
student.close_connection()
