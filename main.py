
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI,  WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse
import asyncio
import uuid
import paho.mqtt.client as paho
from paho import mqtt
import paho.mqtt.client as mqttClient

#app = FastAPI(lifespan=lifespan)
app = FastAPI()

# MQTT client instance
mqtt_client = paho.Client(paho.CallbackAPIVersion.VERSION2,client_id="", userdata=None, protocol=paho.MQTTv5)

# MQTT callback functions
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("Message published with mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} {str(msg.qos)} {str(msg.payload.decode())}")




#MQTT end


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    mqtt_client.username_pw_set("smart_plug", "smartPlug12?")

    # Enable TLS
    mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    # Set the callbacks
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message

    # Connect to the broker
    mqtt_client.connect("20daef8a88f64af88d27eb5f04ad782d.s2.eu.hivemq.cloud", 8883)

    # Subscribe to the topic
    mqtt_client.subscribe("smart_plug/#", qos=1)
    mqtt_client.loop_start()
    yield
    # Clean up the ML models and release the resources
    mqtt_client.loop_stop()
    mqtt_client.disconnect()


app = FastAPI(lifespan=lifespan)


# Serve the HTML for quick testing (optional)
@app.get("/")
async def get():
    mqtt_client.publish("smart_plug/temperature", payload="testing!!!", qos=1)
    return {"hello"}


