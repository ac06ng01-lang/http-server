import os

# file_name = "resources"
# file_name += "/./index.html"
#
# try:
#     with open(file_name, 'rb') as f:
#         file_content = f.read()
# except OSError as e:
#     exit(10)
#
# print(file_content)


strs = "81-100,1-10,20-11,100-102"
ranges = strs.split(',')
lst = None
if len(ranges) == 1:
    vals = ranges[0].split('-')
    print(vals)
    if vals[0] == "":
        if not vals[1].isnumeric():
            print(1)
        lst = int(vals[1]) * -1
    elif vals[1] == "":
        if not vals[0].isnumeric():
            print(2)
        lst = int(vals[0])
    else:
        lst = []
        lst.append([int(value) for value in vals],)

for span in ranges:
    vals = span.split('-')
    print(vals)
    if (not vals[0].isnumeric() or not vals[1].isnumeric()) or int(vals[0]) >= int(vals[1]):
        print(vals[0].isnumeric())
        print(vals[1].isnumeric())
        print(int(vals[0]) >= int(vals[1]))
if isinstance(lst, int):
    print("int")
print(lst)
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
