import socket
import queue
import threading

messages = queue.Queue()

clients = []


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    s.connect(("8.8.8.8", 80)) 
    ip = s.getsockname()[0]

except Exception as e:
    print(f"Error getting local IP: {e}")
    ip = "127.0.0.1"
    
finally:
    s.close()                    


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    server_ip = ip
    server_port = 9999
    server_socket.bind((server_ip, server_port))
    print(f"Server started at {server_ip}:{server_port}")
except OSError as e:
    print(f"Error binding socket: {e}")  


class Server:
    def __init__(self):
        pass

    def receive(self):
        while True:
            try:
                message, addr = server_socket.recvfrom(1024)
                messages.put((message, addr))
            except Exception as e:
                print(f"Receive error: {e}")

    def broadcast(self):
        while True:
            while not messages.empty():
                message, addr = messages.get()
                print(f"Message from {addr}: {message.decode()}")
                if addr not in clients:
                    clients.append(addr)
               
                for client in clients:
                    try:
                        if message.decode().startswith("SIGNUP_TAG:"):
                            name = message.decode()[message.decode().index(":")+1:]
                            server_socket.sendto(f"{name}, joined!".encode(), client)
                        else:
                            server_socket.sendto(message, client)
                    except Exception as e:
                        print(f"Broadcast error: {e}")
                        clients.remove(client)

server_instance = Server()

t1 = threading.Thread(target = server_instance.receive)
t2 = threading.Thread(target = server_instance.broadcast)

t1.start()
t2.start()
