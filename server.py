import socket
import sqlite3

# Создание соединения с базой данных
conn = sqlite3.connect('chat_db.sqlite')
cursor = conn.cursor()

# Создание таблицы для сообщений
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        sender TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')
conn.commit()

# Настройки для сервера
HOST = '127.0.0.1'
PORT = 5555

# Создание сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('Сервер запущен...')
print(f'Хост: {HOST}, Порт: {PORT}')

while True:
    client_socket, client_address = server_socket.accept()
    print(f'Подключено к {client_address}')

    # Обработка сообщений от клиента
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        # Сохранение сообщения в базу данных
        sender, message = data.split(':')
        cursor.execute('INSERT INTO messages (sender, message) VALUES (?, ?)', (sender, message))
        conn.commit()

        # Отправка сообщения всем остальным клиентам
        print(f'{sender}: {message}')
        client_socket.sendall(data.encode())

    client_socket.close()

# Закрытие соединения с базой данных
conn.close()