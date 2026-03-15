import threading, hashlib, os.path
from filelock import FileLock
from os import remove
import time, httpdate
import request_handler, tcp_server
date_string = "Date: {0}\r\n"
thread_local = threading.current_thread().__dict__


def update_date_header(cached_response):
    response_parts = cached_response.split(b"\r\n\r\n")
    position_date = response_parts[0].find(b"Date: ")
    if position_date == -1:
        raise FileNotFoundError("didn't find date header in cached response")
    date_newline = cached_response.find(b"\r\n", position_date)
    if date_newline == -1:
        raise FileNotFoundError("didn't find newline after date header in cached response")
    new_date = httpdate.unixtime_to_httpdate(int(time.time()))
    updated_response = b''.join([cached_response[:position_date + len(b"Date: ")], str(new_date).encode(), cached_response[date_newline:]])
    return updated_response


def save_to_cache(content):
    key = thread_local['CACHE_KEY']
    path = b"cache/" + hashlib.sha1(key).hexdigest().encode()
    try:
        with FileLock(path.decode() + ".lock", thread_local=False):
            with open(path, 'xb') as file:
                file.write(content)
    except FileExistsError:
        # print(f"File keyed {key} already exists in cache")
        with FileLock(path.decode() + ".lock", thread_local=False):
            with open(path, 'r+b') as file:
                if file.read() != content:
                    file.seek(0)
                    file.truncate()
                    file.write(content)


def fetch_from_cache(resource):
    key = thread_local['CACHE_KEY']
    path = b"cache/" + hashlib.sha1(key).hexdigest().encode()

    try:
        with FileLock(path.decode() + ".lock", thread_local=False):
            with open(path, 'rb') as file:
                if os.path.getmtime(resource) >= os.path.getmtime(path):
                    raise ValueError()
                thread_local.pop('CACHE_KEY')
                # print("found in cache:")
                return update_date_header(file.read())

    except ValueError:
        remove(path)
        # print(f"Resource {resource} was updated since caching in {path}")
        raise FileNotFoundError("no file")
    except OSError:
        # print(f"File keyed {key} doesn't exist in cache")
        raise FileNotFoundError("no file")



def modified_since_resolver(resource):
    try:
        if os.path.getmtime(resource) <= thread_local['REQUEST_MODIFIED_SINCE']:
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.NOT_MODIFIED
            raise Exception(request_handler.NOT_MODIFIED)
    except OSError as e:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.NOT_FOUND
        raise Exception("NOT_FOUND")

def unmodified_since_resolver(resource):
    try:
        if os.path.getmtime(resource) >= thread_local['REQUEST_UNMODIFIED_SINCE']:
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.PRECONDITION_FAILED
            raise Exception(request_handler.PRECONDITION_FAILED)
    except OSError as e:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.NOT_FOUND
        raise Exception("NOT_FOUND")


if __name__ == "__main__":
    tcp_server.main()