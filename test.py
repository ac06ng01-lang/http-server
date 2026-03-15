import threading, mimetypes, time, os.path, filelock, random
"""
Fri, 13 Mar 2026 16:47:15 GMT
Tue, 22 Feb 2026 22:00:00 GMT

"""
values = ('127.0.0.1', 16212)

print(':'.join(str(value) for value in values))
# possible_texts = [
#     b"response_constructor.py",
#     b"request_handler.py"
# ]
#
#
# def testing(path):
#     # with filelock.FileLock(path):
#     rand_index = random.randint(0, 1)
#     with open(possible_texts[rand_index], 'rb') as file:
#         to_write = file.read()
#     with open(path, 'w+b') as file:
#         file.write(to_write)
#
#
# file_path = "newfile.txt"
# threads = []
# for i in range(10):
#     threads.append(threading.Thread(target=testing, args=(file_path,)))
#
# for t in threads:
#     t.start()
