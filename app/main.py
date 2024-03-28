import socket
import re
import threading

def http_response(conn):
    data: bytes = conn.recv(1024).decode()
    lines = data.split("\r\n")

    path = lines[0].split(" ")[1]
    echo_keyword = path.split('/')[1]

    user_agent = lines[2].split(" ")[1]

    if path == '/':
        conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
    elif echo_keyword == 'echo':
        pattern = r"/echo/(.*)"
        match = re.search(pattern, path)
        response_body = ""
        if match:
            response_body = match.group(1)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        conn.send(response.encode())
    elif echo_keyword == 'user-agent':
        response_body = user_agent
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        conn.send(response.encode())
    else:
        conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    conn.close()

def main():

    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Received a connection from {client_address}")
        threading.Thread(target=http_response, args=[client_socket]).start()

if __name__ == "__main__":
    main()
