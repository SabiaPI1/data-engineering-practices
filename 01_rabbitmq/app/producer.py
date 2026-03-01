import pika
from app.settings import RABBITMQ_QUEUE, RABBITMQ_HOST

def send_message(message: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE)
        
        channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
        print(f"Sent: {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()