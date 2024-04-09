import pika 


channel = pika.BlockingConnection(pika.ConnectionParameters('localhost')).channel() 
channel.exchange_declare(exchange='exchange', exchange_type='direct')
channel.queue_declare(queue='health check')

channel.queue_bind(exchange='exchange', queue='health check', routing_key='health check')

print("Waiting for messages... press CTRL+C to exit")


def callback(ch, method, properties, body):
    body = body.decode('utf-8')
    print(f"Received message: {body}")

channel.basic_consume(queue='health check', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

