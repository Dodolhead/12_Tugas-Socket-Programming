import tkinter as tk
import socket
import threading
from rsa import *

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message_log_file = "client_messages.txt"

class Client:
    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.name = None

    def write_to_file(self, message):
        with open(message_log_file, "a") as f:
            f.write(message.strip() + "\n")

    def receive(self):
        global chat_box
        while True:
            try:
                message, _ = client.recvfrom(1024)
                decoded_message = message.decode()
                print(decoded_message)
                
                chat_box.insert(tk.END, decoded_message + "\n")
                chat_box.yview(tk.END)

                if not decoded_message.startswith("CheckPass") and not decoded_message.startswith("CheckName"):
                    self.write_to_file(decoded_message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def authenticate_user(self):
        password = password_entry.get()
        client.sendto(f"CheckPass:{password}".encode(), (self.server_ip, self.server_port))
        response, _ = client.recvfrom(1024)
        if response.decode() == "Password accepted.":
            self.hide_password_frame() 
            self.prompt_nickname()
            status_label.config(text="")
        else:
            status_label.config(text="Incorrect password. Try again.")

    def hide_password_frame(self):
        password_frame.pack_forget() 

    def prompt_nickname(self):
        global nickname_entry
        nickname_label.pack(pady=5)
        nickname_entry.pack(pady=5)
        nickname_button.pack(pady=5)

    def set_nickname(self):
        name = nickname_entry.get()
        client.sendto(f"CheckName:{name}".encode(), (self.server_ip, self.server_port))
        response, _ = client.recvfrom(1024)
        if response.decode() == "Nickname has been set.":
            self.name = name
            nickname_label.pack_forget()
            nickname_entry.pack_forget()
            nickname_button.pack_forget()
            status_label.config(text="Kelompok 12 Chat Room")
            status_label.pack(padx=20, pady=20)
            client.sendto(f"Joined:{self.name}".encode(), (self.server_ip, self.server_port))
            self.start_chat()
        else:
            status_label.config(text="Nickname already taken. Please choose another.")

    def start_chat(self):
        chat_frame.pack(padx=10, pady=10)
        message_entry.pack(pady=5)
        send_button.pack(pady=5)
        encrypted_button.pack(pady=5)
        
        t = threading.Thread(target=self.receive)
        t.start()

def connect_to_server():
    global client_instance
    client_instance.server_ip = ip_entry.get()
    client_instance.server_port = int(port_entry.get())
    status_label.config(text=f"Connecting to {client_instance.server_ip}:{client_instance.server_port}...")
    connect_frame.pack_forget()
    password_frame.pack(padx=10, pady=10)

def send_message():
    global message_entry
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    if message == "!q":
        exit()
    else:
        client.sendto(f"{client_instance.name}: {message}".encode(), (client_instance.server_ip, client_instance.server_port))

def send_encrypted_message():
    global message_entry
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    if message == "!q":
        exit()
    else:
        try:
        
            encrypted_message = encrypt(8, message, 65537) 
            encrypted_message_str = ''.join(map(str, encrypted_message))
            client.sendto(f"{client_instance.name}(Encrypted): {encrypted_message_str}".encode(), (client_instance.server_ip, client_instance.server_port))
        except Exception as e:
            print(f"Error encrypting message: {e}")

def main():
    global port_entry, ip_entry, send_button, encrypted_button, client_instance, chat_box, message_entry, nickname_entry, password_entry, status_label, connect_frame, chat_frame, password_frame, nickname_label, nickname_entry, nickname_button
    
    client_instance = Client()

    root = tk.Tk()
    root.title("Client")

    connect_frame = tk.Frame(root)
    connect_frame.pack(padx=10, pady=10)

    ip_label = tk.Label(connect_frame, text="Server IP:")
    ip_label.pack()
    ip_entry = tk.Entry(connect_frame)
    ip_entry.pack()

    port_label = tk.Label(connect_frame, text="Port:")
    port_label.pack()
    port_entry = tk.Entry(connect_frame)
    port_entry.pack()

    connect_button = tk.Button(connect_frame, text="Connect", command=connect_to_server)
    connect_button.pack(pady=5)

    # Password Frame
    password_frame = tk.Frame(root)
    password_label = tk.Label(password_frame, text="Enter Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(password_frame, show="*")
    password_entry.pack(pady=5)
    password_button = tk.Button(password_frame, text="Submit", command=client_instance.authenticate_user)
    password_button.pack(pady=5)

    # Nickname Frame
    nickname_label = tk.Label(root, text="Enter Nickname:")
    nickname_entry = tk.Entry(root)
    nickname_button = tk.Button(root, text="Submit", command=client_instance.set_nickname)

    # Status Label
    status_label = tk.Label(root, text="")
    status_label.pack(pady=5)

    # Chat Frame
    chat_frame = tk.Frame(root)
    chat_box = tk.Text(chat_frame, height=20, width=50)
    chat_box.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(chat_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_box.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=chat_box.yview)

    message_entry = tk.Entry(root, width=50)
    send_button = tk.Button(root, text="Send", command=send_message)
    encrypted_button = tk.Button(root, text="Send Encrypted", command=send_encrypted_message)

    root.mainloop()

main()
