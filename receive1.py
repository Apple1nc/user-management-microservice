import pika

def on_message_recieved(ch, method, properties, body):
    print(f'recieved: "{body}"')
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
channel.queue_declare(queue='mykey')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='myqueue', on_message_callback=on_message_recieved)

print('Start Consuming')

channel.start_consuming()