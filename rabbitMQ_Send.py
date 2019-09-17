#!/usr/bin/env python
import pika
import sys

# Connect to Remote Rabbit Queue
parameters = pika.URLParameters('amqp://xkzcvzvo:kSL8je421PJEAnhXgfRNx2nNcBbRw1UM@impala.rmq.cloudamqp.com/xkzcvzvo')
connection = pika.BlockingConnection(parameters)

# Connect to localhost Rabbit Queue
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare Queue, Creates if it doesnt exist, durable
channel.queue_declare(queue='queue1', durable=True)

# Setup Text to be sent
text = 'Hello World'
if len(sys.argv) > 1:
    text = str(sys.argv[1])


# Sent Items to Queue
channel.basic_publish(exchange='',
                      # Name of The Queue to send to
                      routing_key='queue1',
                      # Data to Send
                      body=text)

print(f" [x] Sent: {text}")

# Close the connection
connection.close()
