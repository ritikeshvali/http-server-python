import socket
import re

def http_response(conn, addr):
    data: bytes = conn.recv(1024).decode()
    lines = data.split("\r\n")

    path = lines[0].split(" ")[1]
    echo_keyword = path.split('/')[1]

    if path == '/':
        conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
    elif echo_keyword != 'echo':
        conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    else:
        pattern = r"/echo/(.*)"
        match = re.search(pattern, path)
        response_body = ""
        if match:
            response_body = match.group(1)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Lenght: {len(response_body)}\r\n\r\n{response_body}"""
        conn.send(response.encode())
    conn.close()

def main():

    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    client_socket, client_address = server_socket.accept()
    print(f"Received a connection from {client_address}")
    http_response(client_socket, client_address)


if __name__ == "__main__":
    main()
