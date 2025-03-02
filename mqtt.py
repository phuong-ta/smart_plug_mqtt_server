import ssl
from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe


# use TLS for secure connection with HiveMQ Cloud
ssl_settings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)

# put in your cluster credentials and hostname
auth = {'username': "smart_plug", 'password': "smartPlug12?"}


# callback to print a message once it arrives
def catch_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))

def publish_msg( topic, message):
    publish.single(
        topic=topic,
        payload=message,
        port=8883,
        client_id="smart_plug",
        auth=auth,
        tls=ssl_settings,
        protocol=paho.MQTTv31,
        hostname="ff561b0054334ef6b26016f2463e72e8.s1.eu.hivemq.cloud"
    )

def init_subscribe():
    subscribe.callback(
        catch_msg,
        topics = "smart_plug/#",
        hostname="ff561b0054334ef6b26016f2463e72e8.s1.eu.hivemq.cloud",
        port=8883,
        auth=auth,
        tls=ssl_settings,
        protocol=paho.MQTTv31
    )
