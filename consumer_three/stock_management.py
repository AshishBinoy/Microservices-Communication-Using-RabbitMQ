import mysql.connector 
import pika 
import time


#Creating MySQL Connection 
mydb = mysql.connector.connect(host = "host.docker.internal", user = "root", password = "root")
cursor = mydb.cursor() 
cursor.execute("CREATE DATABASE IF NOT EXISTS Inventory")
cursor.execute("USE Inventory")

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
channel.queue_declare(queue='stock management')

channel.queue_bind(exchange='exchange', queue='stock management', routing_key='stock management')

# Function to update stock 
def update_stock(item_id,new_quantity):
    cursor.execute("Update Items SET item_quantity = %s WHERE item_id = %s",(new_quantity,item_id))
    mydb.commit()
    print(f"Stock of {item_id} updated to {new_quantity}")

def delete_stock(item_id):
    cursor.execute("DELETE FROM Items WHERE item_id = %s",(item_id,))
    print(f"Item {item_id} deleted from the inventory")
    mydb.commit()

def callback(ch, method, properties, body):     
    print(f"Received message: {body}")
    operation = body.decode('utf-8').split(":")[0]

    if(operation == 'update'):
        item_id, new_quantity = body.decode('utf-8').split(":")[1:]
        update_stock(item_id, new_quantity)
    
    elif(operation == 'delete'):
        item_id = body.decode('utf-8').split(":")[1]
        delete_stock(item_id)

    print("Stock updated")

  
print("Waiting for message... press Ctrl + C to exit.")
channel.basic_consume(queue='stock management', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

