import socket
import threading
import os
import mimetypes
import json

HOST = '0.0.0.0'
PORT = 8080

def handle_client(conn, addr):
    try:
        request = conn.recv(1024).decode()
        if not request:
            conn.close()
            return

        method, path, _ = request.split(' ', 2)

        os.makedirs("logs", exist_ok=True)
        with open("logs/access.log", "a", encoding="utf-8") as log:
            log.write(f"{addr} - {method} {path}\n")

        if method not in ['GET', 'POST']:
            conn.send(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            return

        if method == 'POST' and path == '/api/data':
            body = request.split('\r\n\r\n', 1)[1] if '\r\n\r\n' in request else ''
            response = json.dumps({'received': body})
            conn.send(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode())
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
                    mime += '; charset=utf-8'
                conn.send(f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\nContent-Length: {len(content)}\r\n\r\n".encode() + content)
                conn.send(content)
            else:
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\nFile Not Found")

        else:
            conn.send(b"HTTP/1.1 404 Not Found\r\n\r\nNot Found")

    except Exception as e:
        error_msg = f"Internal Server Error: {e}"
        conn.send(f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: {len(error_msg)}\r\n\r\n{error_msg}".encode())
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listening on {PORT}...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
