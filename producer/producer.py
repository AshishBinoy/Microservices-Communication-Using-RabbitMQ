from flask import Flask
import pika

app = Flask(__name__)


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel() 
channel.exchange_declare(exchange='exchange', exchange_type='direct')

channel.queue_declare(queue='healthcheck')
channel.queue_declare(queue='read')
channel.queue_declare(queue='order_processing')
channel.queue_declare(queue='item_creation')

binding_keys = ['healthcheck', 'read', 'order_processing', 'item_creation']
for binding_key in binding_keys:
    channel.queue_bind(exchange='exchange', queue=binding_key, routing_key=binding_key)



@app.route('/')
def home():
    return "Hello, World"

@app.route('/health_check')
def health_check():
    message = "Health check message sent"

    channel.basic_publish(exchange='exchange', routing_key='healthcheck', body=message)

    return message

@app.route('/read')
def read():
    message = "Message to retrieve all records sent"

    channel.basic_publish(exchange='exchange', routing_key='read', body=message)

    return message

@app.route('/insert/<item_name>/<item_price>/<item_quantity>')
def insert(item_name, item_price, item_quantity):
    message = f"{item_name}:{item_price}:{item_quantity}"

    channel.basic_publish(exchange='exchange', routing_key='item_creation', body=message)

    return message


@app.route('/delete/<item_id>')
def delete(item_id):
    message = f"{item_id}"

    channel.basic_publish(exchange='exchange', routing_key='order_processing', body=message)

    return message  

@app.route('/process_order/<order_id>/<item_id>/<item_quantity>')
def process_order(order_id, item_id, item_quantity):
    message = f"{order_id}:{item_id}:{item_quantity}"

    channel.basic_publish(exchange='exchange', routing_key='order_processing', body=message)

    return f"Order {order_id} for item {item_id} has been processed"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')



