import socket
import threading
import os
import mimetypes
import json

HOST = '0.0.0.0'
PORT = 8080

def handle_client(conn, addr):
    request = conn.recv(1024).decode()
    if not request:
        conn.close()
        return

    try:
        method, path, _ = request.split(' ', 2)
    except:
        conn.close()
        return

    # Basit loglama
    os.makedirs("logs", exist_ok=True)
    with open("logs/access.log", "a", encoding="utf-8") as log:
        log.write(f"{addr} - {path}\n")














    if method != 'GET':
        conn.send(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
        conn.close()
        return

    if path == '/api/hello':
        response = json.dumps({'message': 'Hello from API!'})
        conn.send(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode())
    elif path.startswith('/static'):
        file_path = path.lstrip('/')
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            mime = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            if mime == 'text/html':
                mime += '; charset=utf-8'  # ✅ Türkçe karakterler için kritik düzeltme
            conn.send(f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\nContent-Length: {len(content)}\r\n\r\n".encode() + content)
        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found")
    else:
        conn.send(b"HTTP/1.1 404 Not Found\r\n\r\nNot Found")

    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {PORT}...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

