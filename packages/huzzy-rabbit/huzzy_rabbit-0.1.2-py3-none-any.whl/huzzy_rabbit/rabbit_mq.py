import json
from aio_pika import DeliveryMode, Message, connect, ExchangeType
from aio_pika.abc import AbstractExchange
from typing import Callable

class RabbitMQ:
    exchanges = {}
    channel = None
    # Adding a dummy comment here

    @staticmethod
    async def publish(message_dict: dict, exchange_name: str, routing_key: str, message: Message = None, routing_action: str = None):
        if message is None:

            message_body = json.dumps(message_dict).encode()
            message = Message(
                message_body,
                delivery_mode=DeliveryMode.PERSISTENT,
            )
        
        try:
            exchange: AbstractExchange = RabbitMQ.exchanges[exchange_name]
        except KeyError:
            # exchange = await RabbitMQ.declare_exchange(exchange_name)
            raise Exception(f"Exchange {exchange_name} not found")
        
        message.headers = {
            "action": routing_action
        }
        # Sending the message
        await exchange.publish(message, routing_key=routing_key)

    @staticmethod
    async def connect(connection_url: str):
        # Creating a connection
        # example url = "amqp://guest:guest@localhost/"
        url = connection_url 
        connection = await connect(url)

        # Creating a channel
        RabbitMQ.channel = await connection.channel()
        await RabbitMQ.channel.set_qos(prefetch_count=1)

    @staticmethod
    async def declare_exchange(exchange_name: str):
        exchange = await RabbitMQ.channel.declare_exchange(
            exchange_name,
            type=ExchangeType.DIRECT,
            durable=True,
        )
        # Register exchange
        RabbitMQ.exchanges[exchange_name] = exchange
        return exchange

    @staticmethod
    async def declare_queue_and_bind(queue_name: str, exchange_name: str, app_listener, routing_key: str = None):
        queue = await RabbitMQ.channel.declare_queue(queue_name, durable=True)
 
        try:
            exchange: AbstractExchange = RabbitMQ.exchanges[exchange_name]
        except KeyError:
            # exchange = await RabbitMQ.declare_exchange(exchange_name)
            raise Exception(f"Exchange {exchange_name} not found")

        routing_key = routing_key if routing_key else queue_name

        # Binding the queue to the exchange
        await queue.bind(exchange, routing_key)
        await queue.consume(app_listener)

    @staticmethod
    async def declare_queue(queue_name: str, exchange_name: str, routing_key: str = None):
        queue = await RabbitMQ.channel.declare_queue(queue_name, durable=True)

        try:
            exchange: AbstractExchange = RabbitMQ.exchanges[exchange_name]
        except KeyError:
            # exchange = await RabbitMQ.declare_exchange(exchange_name)
            raise Exception(f"Exchange {exchange_name} not found")
        
        routing_key = routing_key if routing_key else queue_name

        await queue.bind(exchange, routing_key)
        
    async def remote_procedure_call(queue_name: str, on_response: Callable, correlation_id: str, message_dict: dict):
        message_body = json.dumps(message_dict).encode()
        queue = await RabbitMQ.channel.declare_queue(queue_name, durable=True)
        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
            correlation_id=correlation_id,
            reply_to=queue.name,
        )
        await RabbitMQ.publish(
            message=message,
            routing_key="rpc_queue",  
            exchange_name="rpc_exchange", 
            message_dict=message_dict
        )
        await queue.consume(on_response, no_ack=True)