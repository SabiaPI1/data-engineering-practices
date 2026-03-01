from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(
    filename='consumer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

try:
    with open("output.txt", "w") as file:
        print("Consumer is running and listening for messages...")
        logging.info("Consumer started and listening for messages...")
        
        for message in consumer:
            file.write(f"{message.value}\n")
            file.flush() # Принудительно сохраняем в файл
            print(f"Message received: {message.value}")
            logging.info(f"Message received: {message.value}")
except Exception as e:
    logging.error(f"Error occurred: {e}")