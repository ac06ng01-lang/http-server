import socket, threading
import http_server, caching_handler, logger

host = '0.0.0.0'
port = 8888
max_msg_size = 4096

thread_local = threading.current_thread().__dict__

def clean_addr(addr):
    return ':'.join(str(part) for part in addr)


def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    return s

def handle_connection(conn, addr):
    addr = clean_addr(addr)
    thread_local['USER_ADDRESS'] = addr
    data = conn.recv(max_msg_size).decode()
    logger.logger(addr, data, logger.INDEX_REQUEST)
    # print(data)
    response = http_server.request_processing(data)
    conn.send(response)
    logger.logger(addr, response.decode(), logger.INDEX_RESPONSE)
    if 'CACHE_KEY' in thread_local.keys() and 200 <= thread_local['RESPONSE_STATUS_CODE'] < 300:
        caching_handler.save_to_cache(response)
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
        new_thread = threading.Thread(target=handle_connection, args=(connection, client_address))
        new_thread.start()


if __name__ == "__main__":
    main()