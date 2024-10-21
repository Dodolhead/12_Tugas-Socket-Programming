import socket
import threading
import queue

messages = queue.Queue()
clients = [] 
nicknames = [] 
ip = "0.0.0.0"
port = 9999
message_log_file = "messages.txt" 

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, port))
print(f"Server started at {ip}:{port}")
password = "secret"

class Server:
    def __init__(self, server_socket):
        self.server_socket = server_socket

    def write_to_file(self, message):
        with open(message_log_file, "a") as f:
            f.write(message + "\n") 

    def receive(self):
        while True:
            try:
                message, addr = self.server_socket.recvfrom(1024)
                messages.put((message, addr))
            except Exception as e:
                print(f"Error in receive: {e}")

    def broadcast(self):
        while True:
            while not messages.empty():
                message, addr = messages.get()
                decoded_message = message.decode()
                print(decoded_message)

                if not (decoded_message.startswith("CheckPass") or
                        decoded_message.startswith("CheckName") or
                        decoded_message.startswith("Joined")):
                    self.write_to_file(decoded_message)

                if addr not in clients:
                    clients.append(addr)
                    nicknames.append(None) 

                if decoded_message.startswith("Joined"):
                    name = decoded_message.split(":")[1].strip()
                    index = clients.index(addr)
                    nicknames[index] = name
                    self.server_socket.sendto(f"{name} joined!".encode(), addr)
                    for client_addr in clients:
                        if client_addr != addr:
                            self.server_socket.sendto(f"{name} joined the chat!".encode(), client_addr)

                elif decoded_message.startswith("CheckPass"):
                    pw = decoded_message.split(":")[1].strip()
                    if pw != password:
                        self.server_socket.sendto("Incorrect password. Try again".encode(), addr)
                    else:
                        self.server_socket.sendto("Password accepted.".encode(), addr)

                elif decoded_message.startswith("CheckName"):
                    name = decoded_message.split(":")[1].strip()
                    if name in nicknames:
                        self.server_socket.sendto("Nickname already taken.".encode(), addr)
                    else:
                        index = clients.index(addr)
                        nicknames[index] = name
                        self.server_socket.sendto("Nickname has been set.".encode(), addr)

                else:
                    for client_addr in clients:
                        self.server_socket.sendto(message, client_addr)

chat_server = Server(server_socket)

t1 = threading.Thread(target=chat_server.receive)
t2 = threading.Thread(target=chat_server.broadcast)

t1.start()
t2.start()
