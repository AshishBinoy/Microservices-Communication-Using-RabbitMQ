import flask
import pika
import time

app = flask.Flask(__name__)



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

channel.queue_declare(queue='health check')
channel.queue_declare(queue='read')
channel.queue_declare(queue='order processing')
channel.queue_declare(queue='item creation')
channel.queue_declare(queue='stock management')

binding_keys = ['health check', 'read', 'order processing', 'item creation','stock management']
for binding_key in binding_keys:
    channel.queue_bind(exchange='exchange', queue=binding_key, routing_key=binding_key)



@app.route('/')
def home():
    return "Hello, World"

@app.route('/health_check')
def health_check():
    message = "Health check message sent"

    channel.basic_publish(exchange='exchange', routing_key='health check', body=message)

    return message

 @app.route('/read')
 def read():
     message = "Message to retrieve all records sent"
     channel.basic_publish(exchange='exchange', routing_key='read', body=message)
     return message

@app.route('/insert/<item_id>/<item_name>/<item_price>/<item_quantity>')
def insert(item_id,item_name, item_price, item_quantity):
    message = f"{item_id}:{item_name}:{item_price}:{item_quantity}"

    channel.basic_publish(exchange='exchange', routing_key='item creation', body=message)

    return message


@app.route('/delete/<item_id>/')
def delete(item_id):
    message = f"delete:{item_id}"

    channel.basic_publish(exchange='exchange', routing_key='stock management', body=message)

    return message  

@app.route('/update/<item_id>/<quantity>')
def update(item_id,quantity):
    message = f"update:{item_id}:{quantity}"

    channel.basic_publish(exchange='exchange', routing_key='stock management', body=message)

    return message 

@app.route('/process/<order_id>/<item_id>/<item_quantity>')
def orderprocessing(order_id,item_id,item_quantity):
    message = f"{order_id}:{item_id}:{item_quantity}"

    channel.basic_publish(exchange='exchange', routing_key = 'order processing', body=message)

    return message

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')



