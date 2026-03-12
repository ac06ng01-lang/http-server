import threading
import http_server, tcp_server, request_handler

gen_headers = [
    "Server: Moshe\r\n",
    "Content-Type: text/html\r\n",
    "Connection: close\r\n"
]

thread_local = threading.current_thread().__dict__

def create_resp_line(status):
    response_line = " ".join([http_server.version, str(status), http_server.status_codes[status], http_server.new_line])
    return response_line


def construct_headers(status):
    return "".join(gen_headers)


def construct_body(resource):
    try:
        with open(resource, 'rb') as f:
            file_content = f.read()
    except OSError as e:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.NOT_FOUND
        raise Exception("NOT_FOUND")

    if 'REQUEST_RANGE_VALUE' in thread_local.keys():
        ranges = thread_local['REQUEST_RANGE_VALUE']
        file_len = len(file_content)
        partial_content = b""
        if isinstance(ranges, int):
            return file_content[ranges:]
        for range_start, range_end in ranges:
            if range_start < file_len and range_end + 1 <= file_len:
                partial_content += file_content[range_start:range_end + 1]
            else:
                thread_local['RESPONSE_STATUS_CODE'] = request_handler.RANGE_NOT_SATISFIABLE
                raise Exception(http_server.status_codes[request_handler.RANGE_NOT_SATISFIABLE])
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.PARTIAL_CONTENT
        return partial_content
    else:
        return file_content


def create_response(resource=""):
    response_body = b""
    if resource != "":
        try:
            response_body = construct_body(resource)
        except Exception as e:
            print("Exception caught in response constructing:\n%s" % e.args)
    status = thread_local['RESPONSE_STATUS_CODE']
    response_line = create_resp_line(status)
    headers = construct_headers(status)

    return b"".join((response_line.encode(), headers.encode(), http_server.new_line.encode(), response_body))




if __name__ == "__main__":
    tcp_server.main()