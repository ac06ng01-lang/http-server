import socket


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conn = s.connect(('127.0.0.1',8888))
# s.send(b'aaa')
# data = s.recv(1024)
# print(data)

def raiser():
    raise Exception("a", "")


try:
    raiser()

except Exception as e:
    print(e.args)