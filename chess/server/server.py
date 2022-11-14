import socket

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('', 53210))
serv_sock.listen(2)

while True:
    client_sock, client_addr = serv_sock.accept()
    print('Connected by', client_addr)

    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        else:
            print(f'Message: {data.decode("utf-8")}')
        client_sock.sendall(data)

    client_sock.close()