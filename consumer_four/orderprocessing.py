import pika
import mysql.connector 
import time

#Creating MySQL Connection
#Creating MySQL Connection 
mydb = mysql.connector.connect(host = "host.docker.internal", user = "root", password = "root")
cursor = mydb.cursor()
cursor.execute("USE Inventory")
cursor.execute("CREATE TABLE IF NOT EXISTS Orders(order_id INT AUTO_INCREMENT PRIMARY KEY, item_id INT, item_quantity INT, FOREIGN KEY(item_id) REFERENCES Items(item_id) ON DELETE CASCADE ON UPDATE CASCADE)")
mydb.commit()


#Creating RabbitMQ Connection

def connect_to_rabbitmq():
    connection = None
    while connection is None:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ is not ready. Waiting to retry...")
            time.sleep(5)  # wait for 5 seconds before trying to connect again
    return connection

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.exchange_declare(exchange='exchange', exchange_type='direct')
channel.queue_declare(queue='order processing')
channel.queue_bind(exchange='exchange', queue='order processing', routing_key='order processing')

def callback(ch, method, properties, body):
    print("Received message:", body)
    order_id, item_id, item_quantity = body.decode().split(":")
    cursor.execute(f"INSERT INTO Orders VALUES({order_id}, {item_id}, {item_quantity})")
    mydb.commit()
    print(f"Order {order_id} for item {item_id} has been processed")

print("Waiting for messages... press CTRL+C to exit")
channel.basic_consume(queue='order processing', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

