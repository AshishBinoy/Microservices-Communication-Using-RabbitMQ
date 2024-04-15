import mysql.connector 
import pika 

#Creating MySQL Connection 
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "123456789")
cursor = mydb.cursor() 
cursor.execute("USE Inventory")

#Creating RabbitMQ Connection
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
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
    operation, item_id, new_quantity = body.decode('utf-8').split(":")

    if(operation == 'update'):
        update_stock(item_id, new_quantity)
    
    elif(operation == 'delete'):
        delete_stock(item_id)

    print("Stock updated")

  
print("Waiting for message... press Ctrl + C to exit.")
channel.basic_consume(queue='stock management', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

