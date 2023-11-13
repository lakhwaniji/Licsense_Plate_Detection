import paho.mqtt.client as mqtt
import time
import serial
def receive_mqtt_messages(broker_address, topic, client_id="", username="", password="", timeout=2):
    received_messages = []

    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT Broker")
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        received_messages.append(msg.payload.decode())

    client = mqtt.Client(client_id=client_id)
    if username and password:
        client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(broker_address)
        client.loop_start()

        start_time = time.time()
        while time.time() - start_time < timeout:
            time.sleep(10)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        client.disconnect()
        print(received_messages)
        return received_messages[-1]

# Example usage:


def scanning_card():
    arduino = serial.Serial(port='/dev/cu.usbserial-0001', baudrate=9600)
    try:
        data = arduino.readline()
        data = str(data)
        data = data[3:-5]
        return data
    except:
        return "Failure"
    return "12345678"

if __name__ == "__main__":
    #broker_address = "192.168.238.13"  # Replace with your MQTT broker address
    #topic = "bogey_3"  # Replace with your MQTT topic
    #messages = receive_mqtt_messages(broker_address, topic)
    #print(f"Received message: {messages[-1]}")
    print(scanning_card())