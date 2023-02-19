import random

from paho.mqtt import client as mqtt_client
# from serial import Serial
import serial

 
# ser = serial.Serial('COM6', baudrate = 9600, timeout=1)
 
    

broker = 'broker.emqx.io'
port = 1883
# topic0 = "detect/healthy"
# topic1 = "detect/hama"
topic = "detect/Pest"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if (msg.payload.decode() == 'Pest'):
            arduinoData = serial.Serial('COM8',9600)
            data = 1
            arduinoData.write(bytes([data]))
        # print(arduinoData)
        # if (msg.payload.decode("utf-8") ==     '1'):
        #     print('hama')
        # elif(msg.payload.decode("utf-8") == ''):
        #     print('healthy')
        

    client.subscribe(topic)
    # client.subscribe(topic1)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
