
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conn = s.connect(('127.0.0.1',8888))
# s.send(b'aaa')
# data = s.recv(1024)
# print(data)
#
# def raiser():
#     raise Exception("a", "")
#
#
# try:
#     raiser()
#
# except Exception as e:
#     print(e.args)







import socket, threading
#
# host = '127.0.0.1'
# port = 8888
# max_msg_size = 4096
#
# def tcp_server():
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))
#     s.listen(5)
#     return s
#
#
# class ClientThread(threading.Thread):
#
#     def __init__(self, client_ip, client_port, client_sock):
#         threading.Thread.__init__(self)
#         self.ip = ip
#         self.port = port
#         self.sock = client_sock
#
#     def run(self):
#
#
#         data = "dummydata"
#
#         while len(data):
#             data = clientsock.recv(2048)
#             print "Client sent : "+data
#             clientsock.send("You sent me : "+data)
#
#
#
# tcpsock = tcp_server()
# threads = []
#
#
# while True:
#     (clientsock, (ip, port)) = tcpsock.accept()
#     newthread = ClientThread(ip, port, clientsock)
#     newthread.start()
#     threads.append(newthread)
#
# for t in threads:
#     t.join()
#
#
