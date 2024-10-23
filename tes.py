import tkinter as tk
from tkinter import simpledialog
import threading
import socket  # Assuming you use sockets for communication

# Create global variables for socket communication
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_ip = "127.0.0.1"  # Replace with your server's IP address
password = "your_password"  # Replace with your actual password
is_authenticated = False

class Client:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        
        # Create chat display area
        self.chat_display = tk.Text(root, state='disabled', width=50, height=20)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10)

        # Create input field for messages
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        # Create send button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=0, pady=10)

        # Start the authentication process
        self.authenticate_user()

    def authenticate_user(self):
        global is_authenticated
        while not is_authenticated:
            entered_password = simpledialog.askstring("Password", "Enter password:", show='*')
            if entered_password == password:
                is_authenticated = True
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, "Password accepted.\n")
                self.chat_display.config(state='disabled')
            else:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, "Incorrect password. Try again.\n")
                self.chat_display.config(state='disabled')

    def receive(self):
        while True:
            try:
                message, _ = client.recvfrom(1024)
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, message.decode() + "\n")
                self.chat_display.config(state='disabled')
                self.chat_display.see(tk.END)
            except Exception as e:
                print(f"Error receiving message: {e}")

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message == "!q":
            self.root.quit()
        else:
            client.sendto(f"{name}: {message}".encode(), (server_ip, 9999))
            self.message_entry.delete(0, tk.END)

# Initialize Tkinter and create the chat client
root = tk.Tk()
client_instance = Client(root)

# Ask for the user's nickname
name = simpledialog.askstring("Nickname", "Enter your nickname:")

# Start the thread for receiving messages
t = threading.Thread(target=client_instance.receive)
t.daemon = True
t.start()

# Send a message indicating that the user has joined
client.sendto(f"Joined: {name}".encode(), (server_ip, 9999))

# Start the Tkinter main loop
root.mainloop()
