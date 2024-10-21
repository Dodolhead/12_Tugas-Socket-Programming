import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = input("Masukkan IP: ")
server_port = int(input("Masukkan Port: "))
client.bind((server_ip, server_port))
print(f"Client started at {server_ip}:{server_port}")
message_log_file = "client_messages.txt"

class Client:
    def __init__(self):
        pass

    def write_to_file(self, message):
        with open(message_log_file, "a") as f:
            f.write(message + "\n")

    def receive(self):
        while True:
            try:
                message, _ = client.recvfrom(1024)
                decoded_message = message.decode()
                print(decoded_message)

                if not decoded_message.startswith("CheckPass") and not decoded_message.startswith("CheckName"):
                    self.write_to_file(decoded_message) 

            except Exception as e:
                print(f"Error receiving message: {e}")

    def authenticate_user(self):
        is_authenticated = False
        while not is_authenticated:
            password = input("Enter password: ")
            client.sendto(f"CheckPass:{password}".encode(), (server_ip, 9999))
            response, _ = client.recvfrom(1024) 
            if response.decode() == "Password accepted.":
                is_authenticated = True
            else:
                print("Incorrect password. Try again.")

    def set_nickname(self):
        is_taken = True
        while is_taken:
            name = input("Nickname: ")
            client.sendto(f"CheckName:{name}".encode(), (server_ip, 9999))
            response, _ = client.recvfrom(1024)

            if response.decode() == "Nickname has been set.":
                is_taken = False
            else:
                print("Nickname already taken. Please choose another.")

        return name

client_instance = Client()
client_instance.authenticate_user()
name = client_instance.set_nickname()
t = threading.Thread(target=client_instance.receive)
t.start()

client.sendto(f"Joined:{name}".encode(), (server_ip, 9999))

while True:
    message = input("")
    if message == "!q":
        exit()
    else:
        client.sendto(f"{name}: {message}".encode(), (server_ip, 9999))
