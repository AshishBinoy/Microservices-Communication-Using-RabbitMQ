import flask
import pika

app = flask.Flask(__name__)


# TODO: Add this after RabbitMQ is setup
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel() 
# channel.exchange_declare(exchange='exchange', exchange_type='direct')

# channel.queue_declare(queue='healthcheck')
# channel.queue_declare(queue='read')
# channel.queue_declare(queue='order_processing')
# channel.queue_declare(queue='item_creation')

# binding_keys = ['healthcheck', 'read', 'order_processing', 'item_creation']
# for binding_key in binding_keys:
#     channel.queue_bind(exchange='exchange', queue=binding_key, routing_key=binding_key)



@app.route('/')
def home():
    return "Hello, World"

@app.route('/health_check')
def health_check():
    message = "Health check message sent"

    # TODO: Add this after RabbitMQ is setup
    # channel.basic_publish(exchange='exchange', routing_key='healthcheck', body=message)

    return message

@app.route('/read')
def read():
    message = "Message to retrieve all records sent"

    # TODO: Add this after RabbitMQ is setup
    # channel.basic_publish(exchange='exchange', routing_key='read', body=message)

    return message

@app.route('/insert/<item_name>/<item_price>/<item_quantity>')
def insert(item_name, item_price, item_quantity):
    message = f"{item_name}:{item_price}:{item_quantity}"

    # TODO: Add this after RabbitMQ is setup
    # channel.basic_publish(exchange='exchange', routing_key='item_creation', body=message)

    return message


@app.route('/delete/<item_id>')
def delete(item_id):
    message = f"{item_id}"

    # TODO: Add this after RabbitMQ is setup
    # channel.basic_publish(exchange='exchange', routing_key='order_processing', body=message)

    return message  


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



