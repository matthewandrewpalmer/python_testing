#!/usr/bin/env python
import pika

# Connect to Remote Rabbit Queue
parameters = pika.URLParameters('amqp://xkzcvzvo:kSL8je421PJEAnhXgfRNx2nNcBbRw1UM@impala.rmq.cloudamqp.com/xkzcvzvo')
connection = pika.BlockingConnection(parameters)
# Connect to localhost Rabbit Queue
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare Queue, Creates if it doesnt exist, durable
channel.queue_declare(queue='queue1', durable=True)


# Method called when item is received
def callback(ch, method, properties, body):
    print(method)
    print(f" [x] Received : {body}")


# Receive Item from Queue
channel.basic_consume(queue='queue1',
                      # If True then Callback will send to Rabbit that the server (This script) has received
                      # the data, so the item to be removed from the queue
                      # IF False then the data will remain in the Queue
                      auto_ack=True,
                      # When item is received run the function Callback
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# Close the connection
connection.close()
