# ipc_client.py

import os
import re
import sys
import json
import paho.mqtt.client as mqtt
import traceback
from typing import Callable, Dict
from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import PublishMessage, JsonMessage
from awsiot.greengrasscoreipc.model import (
    SubscriptionResponseMessage,
    UnauthorizedError,
    IoTCoreMessage
)

class BaseIPCClient:

    _instance = None
    subscribed_topics = []
    CallbackType = Callable[[str, dict], None]
    callbacks: Dict[str, CallbackType] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseIPCClient, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        raise NotImplementedError("Initialize method not implemented")

    def publish(self, topic, message):
        raise NotImplementedError("Publish method not implemented")

    def subscribe(self, topic, callback: CallbackType = None):
        raise NotImplementedError("Subscribe method not implemented")

    def on_stream_event(self, topic: str, message: dict):
        for pattern, callback in self.callbacks.items():
            if re.match(pattern, topic) and callback is not None:
                callback(topic, message)
                return

    def on_stream_error(self, error):
        print("Stream error {}".format(error))

    def on_stream_closed(self, topics=[str]):
        print("Stream closed for topics {}".format(topics))

    @staticmethod
    def parse_pattern(topic: str) -> bool:
        escaped_pattern = topic.replace(".", "\\.")
        regex_pattern = re.compile(
            escaped_pattern.replace("+", "[^/]+").replace("#", ".*"))
        return regex_pattern

    def map_topic_to_callback(self, topic: str, callback: CallbackType):
        topic_pattern = BaseIPCClient.parse_pattern(topic)
        self.callbacks[topic_pattern] = callback


# Local MQTT Client for publishing messages to MQTT topics locally for testing/debugging
class LocalMQTTPublisher(BaseIPCClient):
    def _initialize(self, broker_address=os.getenv("BROKER_HOSTNAME"), port=1883):
        self.client = mqtt.Client()
        self.client.connect(broker_address, port, 60)
        self.client.on_socket_close = self.on_closed
        self.client.on_disconnect = self.on_closed
        self.client.loop_start()

    def publish(self, topic, message):
        if message == '':
            message = {}
        json_message = json.dumps(message)
        self.client.publish(topic=topic, payload=json_message, qos=1)

    def subscribe(self, topic, callback=None):
        self.map_topic_to_callback(topic, callback)
        self.client.subscribe(topic, qos=1)
        self.client.on_message = self.on_message
        self.client.on_socket_close = self.on_closed
        self.subscribed_topics.append(topic)

    def on_message(self, client, userdata, message: mqtt.MQTTMessage):
        payload = message.payload if message.payload != None and len(
            message.payload) > 0 else "{}"
        json_message = json.loads(payload)
        self.on_stream_event(message.topic, json_message)
        # convert bytes array to json

    # not an existing equivalent for paho.mqtt.client, so might not need this
    def on_error(self, client, userdata, message):
        self.on_stream_error(message.payload, message.topic)

    def on_closed(self, client, userdata, rc):
        self.on_stream_closed()

# Greengrass IPC Client for publishing messages to MQTT topics locally in Greengrass environment


class GreengrassIPCClient(BaseIPCClient):
    def _initialize(self):
        self.client = GreengrassCoreIPCClientV2()

    def publish(self, topic, message):
        if message == '':
            message = {}
        json_message_aws = JsonMessage(message=message)
        json_message = PublishMessage(json_message=json_message_aws)
        operation = self.client.publish_to_topic_async(
            topic=topic, publish_message=json_message)
        print("Operation Status: {}".format(operation))

    def subscribe(self, topic, callback=None):
        self.map_topic_to_callback(topic, callback)
        resp, operation = self.client.subscribe_to_topic_async(
            topic=topic, on_stream_event=self.on_message, on_stream_error=self.on_error, on_stream_closed=self.on_closed)
        self.subscribed_topics.append(topic)

    def on_message(self, event: SubscriptionResponseMessage) -> None:
        try:
            if event.json_message:
                message = event.json_message.message if event.json_message.message != None and len(
                    event.json_message.message) > 0 else "{}"
                if isinstance(message, str):
                    message = json.loads(message)  # Ensures string is converted to dict
                topic = event.json_message.context.topic
                self.on_stream_event(topic, message)
            elif event.binary_message:
                message = str(event.binary_message.message, 'utf-8')  # Decode bytes to string
                try:
                    message = json.loads(message)  # Attempt to parse JSON
                except json.JSONDecodeError:
                    print("Received non-JSON message, handling as raw text.")
                topic = event.binary_message.context.topic
                self.on_stream_event(topic, message)
        except Exception as e:
            print(f"Error processing message: {e}")
            traceback.print_exc()

    def on_error(self, error: Exception) -> bool:
        print('Received a stream error.', file=sys.stderr)
        self.on_stream_error(error)
        traceback.print_exc()
        return False  # Return True to close stream, False to keep stream open.

    def on_closed(self) -> None:
        self.on_stream_closed()
        print('Subscribe to topic stream closed.')

# Greengrass Client for publishing messages AWS IoT Core MQTT topics in Greengrass environment


class GreengrassIoTClient(BaseIPCClient):
    def _initialize(self):
        self.client = GreengrassCoreIPCClientV2()

    def publish(self, topic, message):
        if message == '':
            message = {}
        json_message = json.dumps(message)
        operation = self.client.publish_to_iot_core_async(
            topic_name=topic, qos='1', payload=json_message)

    def subscribe(self, topic, callback=None):
        self.map_topic_to_callback(topic, callback)
        self.client.subscribe_to_iot_core_async(
            topic_name=topic, qos='1', on_stream_event=self.on_message, on_stream_error=self.on_error, on_stream_closed=self.on_closed)
        self.subscribed_topics.append(topic)

    def on_message(self, event: IoTCoreMessage) -> None:
        try:
            message = event.message.payload if event.message != None and event.message.payload != None and len(
                event.message.payload) > 0 else b"{}"
            message = str(message, 'utf-8')
            message = json.loads(message)
            topic = event.message.topic_name
            self.on_stream_event(topic, message)
        except:
            traceback.print_exc()

    def on_error(error: Exception) -> bool:
        print('Received a stream error.', file=sys.stderr)
        traceback.print_exc()
        return False  # Return True to close stream, False to keep stream open.

    def on_closed() -> None:
        print('Subscribe to topic stream closed.')

# Used to publish messages to MQTT topics locally in Greengrass environment


def get_ipc_client():
    # Use LocalMQTTPublisher for local testing if DEBUG is set
    if os.getenv('DEBUG') != None and os.getenv('DEBUG').lower() == 'true':
        return LocalMQTTPublisher()
    else:
        # Default to GreengrassIPCClient for production environment
        return GreengrassIPCClient()

# Used to publish messages to AWS IoT Core MQTT topics


def get_iot_client():
    # Use LocalMQTTPublisher for local testing if DEBUG is set
    if os.getenv('DEBUG') != None and os.getenv('DEBUG') == 'true':
        return LocalMQTTPublisher()
    else:
        # Default to GreengrassMQTTClient for production environment
        return GreengrassIoTClient()
