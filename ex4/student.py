import json
import time

import pika


class Student:
    def __init__(self, student_id):
        self.student_id = student_id
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange="assignment_exchange", exchange_type="direct")

    def submit_assignment(self, module, answer):
        assignment = {"student_id": self.student_id, "module": module, "answer": answer, "status": "submitted"}
        self.channel.basic_publish(
            exchange="assignment_exchange",
            routing_key=f"{module}_queue",
            body=json.dumps(assignment).encode("utf-8")
        )
        print(f"Student {self.student_id}: Assignment submitted for {module}")

    def close_connection(self):
        print(f"Student {self.student_id}: Connection closed")
        self.channel.stop_consuming()
        self.connection.close()


time.sleep(3)
student_cc = Student(student_id="123")
student_dm = Student(student_id="456")

time.sleep(5)
student_cc.submit_assignment(module="cloud_computing", answer="CC answer")
student_dm.submit_assignment(module="data_mining", answer="DM answer")

time.sleep(3)
student_cc.close_connection()
student_dm.close_connection()
