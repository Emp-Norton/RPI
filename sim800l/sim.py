import serial
import time
import os

from openai import OpenAI
from decouple import config

oaikey = config('OAIKEY')

class SIM800Module:
    def __init__(self, port="/dev/serial0", baudrate=115000):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        self.isConnected = False

    def connect(self):
        if not self.ser.is_open:
            self.ser.open()
            self.ser.write(b"AT\r\n")
            response = self.ser.readlines()
            if "OK" in str(response):
                self.isConnected = True
                print("Connected to SIM800 module.")
            else:
                print("Failed to connect to SIM800 module.")

    def check_status(self):
        if self.isConnected:
            self.ser.write(b"AT+CSQ\r\n")
            response = self.ser.readlines()
            print("Signal Quality: ", response[1].decode("utf-8").strip())
        else:
            print("Not connected to SIM800 module.")

    def send_message(self, recipient_number, message):
        if self.isConnected:
            self.ser.write(b"AT+CMGF=1\r\n")
            time.sleep(0.5)
            self.ser.write(b'AT+CMGS="' + recipient_number.encode() + b'"\r\n')
            time.sleep(0.5)
            self.ser.write(message.encode() + b"\r\n")
            time.sleep(0.5)
            self.ser.write(b"\x1A")
            response = self.ser.readlines()
            if "OK" in str(response):
                print("Message sent successfully.")
            else:
                print("Failed to send message.")
        else:
            print("Not connected to SIM800 module.")

    def read_messages(self):
        if self.isConnected:
            self.ser.write(b'AT+CMGL="ALL"\r\n')
            response = self.ser.readlines()
            for line in response:
                print(line.decode("utf-8").strip())
        else:
            print("Not connected to SIM800 module.")

    def delete_message(self, index):
        if self.isConnected:
            self.ser.write(b"AT+CMGD=" + str(index).encode() + b"\r\n")
            response = self.ser.readlines()
            if "OK" in str(response):
                print("Message deleted successfully.")
            else:
                print("Failed to delete message.")
        else:
            print("Not connected to SIM800 module.")

    def disconnect(self):
        if self.isConnected:
            self.ser.close()
            self.isConnected = False
            print("Disconnected from SIM800 module.")
        else:
            print("Not connected to SIM800 module.")




class OpenAIFormatter:
    def __init__(self, key=oaikey, model='gpt-4-turbo'):
        self.model = model
        self.client = self._handle_credentials(key)

    def _handle_credentials(self, key):
        return OpenAI(api_key=key)

    def format_prompt(self, message, **kwargs):
        msg_obj = {'role':'user', 'content':message}
        return msg_obj

    def send_prompt(self, prompt):
        formatted_msg = self.format_prompt(prompt)
        r = self.client.chat.completions.create(model=self.model,messages=[formatted_msg])
        return r.choices[0].message.content

if __name__ == "__main__":
    sim_module = SIM800Module()
    sim_module.connect()
    sim_module.check_status()

