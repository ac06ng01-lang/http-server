import socket, select, http_server

host = '127.0.0.1'
port = 8888
max_msg_size = 4096

def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    return s


def main():
    server = tcp_server()
    client_sockets = []
    while True:
        rlist, wlist, xlist = select.select([server] + client_sockets, [], [])
        for current_socket in rlist:
            if current_socket is server:
                connection, client_address = current_socket.accept()
                # print("New client joined!", client_address)
                client_sockets.append(connection)
            else:
                data = current_socket.recv(max_msg_size).decode()
                response = http_server.request_processing(data)
                print(response.decode())
                current_socket.send(response)
                client_sockets.remove(current_socket)
                current_socket.close()


if __name__ == "__main__":
    main()