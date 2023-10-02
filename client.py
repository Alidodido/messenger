import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog  # Import simpledialog for asking username

def send_message():
    message = message_input.get()
    if message:
        formatted_message = "-> " + username + ": " + message
        message_text.configure(state="normal")
        message_text.insert(END, formatted_message + '\n', 'user_message')  # Display the user message in light green
        client_socket.send(formatted_message.encode('utf-8'))
        message_input.delete(0, END)  # Clear the message input field
        message_text.see(END)  # Auto-scroll to the end
        message_text.configure(state="disabled")

def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            message_text.configure(state="normal")
            if message.startswith("-> " + username):
                # User's own message, highlight in light green
                message_text.insert(END, message + '\n', 'user_message')
            else:
                # Other users' messages, highlight in dark green
                message_text.insert(END, message + '\n', 'other_message')
            message_text.see(END)  # Auto-scroll to the end
            message_text.configure(state="disabled")
        except:
            # Handle any errors here
            break

# Create a pop-up dialog to get the username

roomIP = simpledialog.askstring("Room IP","Enter your room IP: ")
username = simpledialog.askstring("Username", "Enter your username:")

# Create the main chat window
win = Tk()
win.title("Codidodido Chat")
win.resizable(False,False)


greeting_text = ttk.Label(win, text=f"Welcome {username}")
greeting_text.pack()

message_text = Text(win, width=50, height=20, wrap=WORD, state="disabled")
message_text.pack()

# Define text tags for user's messages and other messages
message_text.tag_configure('user_message', background='green')
message_text.tag_configure('other_message', background='blue',foreground="white")

message_box = LabelFrame(win, text=f"{username} Message: ")
message_box.pack()

message_input = ttk.Entry(message_box, width=40)
message_input.grid(row=0, column=0)

send_button = ttk.Button(message_box, text="Send", command=send_message)
send_button.grid(row=0, column=1)

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port to connect to
server_address = (roomIP, 12345)

# Connect to the server
client_socket.connect(server_address)

# Create threads for sending and receiving messages
receive_thread = threading.Thread(target=receive_message, daemon=True)

# Start the receiving thread
receive_thread.start()

win.mainloop()
