import socket
import threading
import random
import tkinter as tk

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.connect(("8.8.8.8", 80)) 
    ip = s.getsockname()[0]

except Exception as e:
    print(f"Error getting local IP: {e}")
    ip = "127.0.0.1"
    
finally:
    s.close()       

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    server_ip = ip
    server_port = random.randint(8000,9999)
    client.bind((server_ip, server_port))
    print(f"Server started at {server_ip}:{server_port}")
except OSError as e:
    print(f"Error binding socket: {e}")  

name = input("Nickname: ")

class Client:
    def __init__(self):
        pass

    def receive(self):
        while True:
            try:
                message, _ = client.recvfrom(1024)
                print(message.decode())
            except:
                pass

client_instance = Client()

t = threading.Thread(target = client_instance.receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), (server_ip, 9999))

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), ((server_ip, 9999)))
