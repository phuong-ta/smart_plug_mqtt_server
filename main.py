import asyncio
import paho.mqtt.client as paho
from paho import mqtt
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager

MQTT_BROKER = "20daef8a88f64af88d27eb5f04ad782d.s2.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "smart_plug/temperature"
MQTT_USERNAME = "smart_plug"
MQTT_PASSWORD = "smartPlug12?"

mqtt_client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
message_queue = asyncio.Queue()  # Store received messages asynchronously

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected to MQTT Broker with code {rc}")
    client.subscribe(MQTT_TOPIC, qos=1)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} - {msg.payload.decode()}")
    asyncio.create_task(message_queue.put(msg.payload.decode()))  # Store message in queue

def on_publish(client, userdata, mid, properties=None):
    print(f"Message published (MID: {mid})")

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed: {mid} {granted_qos}")

# Background MQTT Listener
async def mqtt_loop():
    while True:
        mqtt_client.loop(timeout=1.0)  # Process network traffic
        await asyncio.sleep(0.1)  # Prevent blocking the event loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting MQTT Client...")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_publish = on_publish
    mqtt_client.on_subscribe = on_subscribe
    
    mqtt_client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

    task = asyncio.create_task(mqtt_loop())  # Start MQTT loop in the background
    yield
    print("Stopping MQTT Client...")
    task.cancel()
    mqtt_client.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "FastAPI MQTT Server Running"}

@app.post("/publish/")
async def publish_message(topic: str = MQTT_TOPIC, message: str = "Hello MQTT"):
    mqtt_client.publish(topic, payload=message, qos=1)
    return {"status": "Message Sent", "topic": topic, "message": message}

@app.get("/messages/")
async def get_messages():
    messages = []
    while not message_queue.empty():
        messages.append(await message_queue.get())  # Retrieve all messages
    return {"received_messages": messages}
