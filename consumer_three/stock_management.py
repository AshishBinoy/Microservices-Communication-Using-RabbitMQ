import mysql.connector 
import pika 



#Creating MySQL Connection 
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "123456789")
cursor = mydb.cursor() 
cursor.execute("USE Inventory")

#Creating RabbitMQ Connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='exchange', exchange_type='direct')
channel.queue_declare(queue='stock')

channel.queue_bind(exchange='exchange', queue='stock', routing_key='stock')

# Function to update stock 

def callback(ch, method, properties, body):     
    print(f"Received message: {body}")
    item_id, item_name, item_price, item_quantity = body.decode('utf-8').split(":")
    cursor.execute("UPDATE Items SET item_quantity = %s WHERE item_id = %s", (item_quantity, item_id))
    mydb.commit()
    print(f"Stock of {item_name} updated to {item_quantity}")



print("Waiting for message... press Ctrl + C to exit.")
channel.basic_consume(queue='stock', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

