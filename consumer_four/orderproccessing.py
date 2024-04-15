import pika
import mysql.connector 

#Creating MySQL Connection
mydb = mysql.connector.connect(host = "mysql", user = "root", password = "123456789")
cursor = mydb.cursor()
cursor.execute("USE Inventory")
cursor.execute("CREATE TABLE IF NOT EXISTS Orders(order_id INT AUTO_INCREMENT PRIMARY KEY, item_id INT, item_quantity INT, FOREIGN KEY(item_id) REFERENCES Items(item_id) ON DELETE CASCADE ON UPDATE CASCADE)")
mydb.commit()


#Creating RabbitMQ Connection
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
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

