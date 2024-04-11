import socket
import tkinter as tk
import threading
from tkinter import simpledialog

askname = name = simpledialog.askstring("Чат", "Как вас звать?")

# Функция для отправки сообщений
def send_message(event=None):
    message = message_entry.get()
    sender = askname
    msg = f'{sender}: {message}'
    client_socket.sendall(msg.encode())
    message_entry.delete(0, tk.END)

# Функция для получения сообщений от сервера
def receive_messages():
    while True:
        data = client_socket.recv(1024).decode()
        messages_text.insert(tk.END, data + '\n')

HOST = '127.0.0.1'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

root = tk.Tk()
root.title('Чат')

message_frame = tk.Frame(root)
message_frame.pack(pady=10)

messages_text = tk.Text(message_frame, height=20, width=50)
messages_text.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(message_frame, command=messages_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
messages_text.config(yscrollcommand=scrollbar.set)

message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)

send_button = tk.Button(root, text='Отправить', command=send_message)
send_button.pack()

message_entry.bind("<Return>", send_message)

# Запуск потока для получения сообщений от сервера
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

root.mainloop()