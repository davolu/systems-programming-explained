import socket, threading

HOST, PORT = "127.0.0.1", 0              # 0 = let the OS pick a free port

def parse(message):
    command, _, body = message.partition(" ")
    return command, body

def handle(conn):
    data = conn.recv(1024).decode()
    command, body = parse(data.strip())
    if command == "REQUEST":
        conn.sendall(f"RESPONSE {body}".encode())
    else:
        conn.sendall(b"ERROR unknown command")
    conn.close()

def server(sock):
    conn, _ = sock.accept()
    handle(conn)

sock = socket.socket(); sock.bind((HOST, PORT)); sock.listen(1)
port = sock.getsockname()[1]
t = threading.Thread(target=server, args=(sock,)); t.start()

client = socket.create_connection((HOST, port))
client.sendall(b"REQUEST hello")
reply = client.recv(1024).decode()
client.close(); t.join(); sock.close()

command, body = parse(reply)
print(f"sent:    REQUEST hello")
print(f"parsed:  command={command!r}, body={body!r}")
print(f"reply:   {reply}")
