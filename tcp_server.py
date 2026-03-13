import socket, threading
import http_server, caching_handler

host = '127.0.0.1'
port = 8888
max_msg_size = 4096

thread_local = threading.current_thread().__dict__

def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    return s

def handle_connection(conn):
    data = conn.recv(max_msg_size).decode()
    # print(data)
    response = http_server.request_processing(data)
    conn.send(response)
    if 'CACHE_KEY' in thread_local.keys() and 200 <= thread_local['RESPONSE_STATUS_CODE'] < 300:
        caching_handler.save_to_cache(response)
    print("\n\nResponse sent:\n" + response.decode())
    conn.close()
    to_be_removed = []
    for key in thread_local.keys():
        if not key.startswith('_'):
            to_be_removed.append(key)
    for key in to_be_removed:
        thread_local.pop(key)

def main():
    server = tcp_server()
    while True:
        connection, client_address = server.accept()
        new_thread = threading.Thread(target=handle_connection, args=(connection,))
        new_thread.start()


if __name__ == "__main__":
    main()