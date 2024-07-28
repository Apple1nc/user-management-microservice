# from __future__ import absolute_import, unicode_literals

# import os

# import kombu
# from celery import Celery, bootsteps

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users.settings')

# app = Celery('users')


# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks()


# #setting publisher
# with app.pool.acquire(block=True) as conn:
#     exchange = kombu.Exchange(
#         name='myexchange',
#         type='direct',
#         durable=True,
#         channel=conn,
#     )
#     exchange.declare()

#     queue = kombu.Queue(
#         name='myqueue',
#         exchange=exchange,
#         routing_key='mykey',
#         channel=conn,
#         message_ttl=600,
#         queue_argumnets={
#             'x-queue-type': 'classic'
#         },
#         durable=True
#     )
#     queue.declare()


#     #setting consumer
#     class MyConsumerStep(bootsteps.ConsumerStep):

#         def get_consumers(self, channel):
#             return [kombu.Consumer(channel,
#                                    queues=[queue],
#                                    callbacks=[self.handle_message],
#                                    accept=['json'])]
        
#         def handle_message(self, body, message):
#             print('Received message: {0!r}'.format(body))
#             message.ack()


# app.steps['consumer'].add(MyConsumerStep)


from __future__ import absolute_import, unicode_literals

import os
from celery import Celery, bootsteps
from kombu import Exchange, Queue, Consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users.settings')

app = Celery('users')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# Namespace 'CELERY' means all celery-related configuration keys
# should have a 'CELERY_' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# Create and declare exchanges and queues
with app.pool.acquire(block=True) as conn:
    listing_exchange = Exchange(
        name='listing_exchange',
        type='topic',
        durable=True,
        channel=conn,
    )
    listing_exchange.declare()

    listing_queue = Queue(
        name='listing_queue',
        exchange=listing_exchange,
        routing_key='shop.created',
        channel=conn,
        queue_arguments={'x-queue-type': 'classic'},
        durable=True
    )
    listing_queue.declare()


# Define custom consumer step for handling messages
class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        # Define multiple queues
        listing_queue = Queue('listing_queue', Exchange('listing_exchange', type='direct'), routing_key='shop.created')

        return [
            Consumer(channel,
                     queues=[listing_queue],
                     callbacks=[self.handle_listing_message],
                     accept=['json'])
        ]


    def handle_listing_message(self, body, message):
        print('Received listing message: {0!r}'.format(body))
        # Add your handling logic for listing messages here
        message.ack()

app.steps['consumer'].add(MyConsumerStep)
