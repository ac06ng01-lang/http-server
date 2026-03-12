import threading, httpdate, time, mimetypes
import http_server, tcp_server, request_handler

gen_headers = [
    "Server: Moshe\r\n",
    "Connection: close\r\n",
]

content_length_string = "Content-Length: {0}\r\n"
date_string = "Date: {0}\r\n"
boundary_string = "SEPARATING_STRING"
multipart_content_type_value = "multipart/byteranges; boundary=" + boundary_string
multipart_prefix_string = "--"+ boundary_string + "\r\n{0}{1}"
content_range_string = "Content-Range: bytes {0}-{1}/{2}\r\n"
content_type_string = "Content-Type: {0}\r\n"

thread_local = threading.current_thread().__dict__

def create_resp_line(status):
    response_line = " ".join([http_server.version, str(status), http_server.status_codes[status], http_server.new_line])
    return response_line


def construct_headers(status):
    return "".join(gen_headers)

def get_content_type(resource):
    return mimetypes.guess_type(resource)[0] or "text/html"


def construct_body(resource):
    try:
        with open(resource, 'rb') as f:
            file_content = f.read()
    except OSError as e:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.NOT_FOUND
        raise Exception("NOT_FOUND")

    content_type = content_type_string.format(get_content_type(resource))
    file_len = len(file_content)

    thread_local['HEADER-CONTENT_TYPE'] = content_type
    thread_local['HEADER-DATE'] = date_string.format(httpdate.unixtime_to_httpdate(int(time.time())))

    if 'REQUEST_RANGE_VALUE' in thread_local.keys():
        ranges = thread_local['REQUEST_RANGE_VALUE']
        partial_content = b""
        if isinstance(ranges, int):
            partial_content = file_content[ranges:]
            if ranges < 0:
                ranges = file_len - 1 + ranges
            thread_local['HEADER-CONTENT_RANGE'] = content_range_string.format(ranges, file_len - 1, file_len,)
            thread_local['HEADER-CONTENT_LENGTH'] = content_length_string.format(len(partial_content))
            return partial_content

        for range_start, range_end in ranges:
            if range_start < file_len and range_end + 1 <= file_len:
                if 'SINGLE_PART_BODY' not in thread_local.keys():
                    partial_content += multipart_prefix_string.format(content_type, content_range_string.format(range_start, range_end, file_len,),).encode()
                partial_content += file_content[range_start:range_end + 1]
                if 'SINGLE_PART_BODY' not in thread_local.keys():
                    partial_content += b"\r\n"

            else:
                thread_local['RESPONSE_STATUS_CODE'] = request_handler.RANGE_NOT_SATISFIABLE
                raise Exception(http_server.status_codes[request_handler.RANGE_NOT_SATISFIABLE])

        thread_local['RESPONSE_STATUS_CODE'] = request_handler.PARTIAL_CONTENT
        if 'SINGLE_PART_BODY' not in thread_local.keys():
            thread_local['HEADER-CONTENT_TYPE'] = content_type_string.format(multipart_content_type_value)
            partial_content += b"--" + boundary_string.encode() + b"--"
        thread_local['HEADER-CONTENT_LENGTH'] = content_length_string.format(len(partial_content))
        return partial_content
    else:
        thread_local['HEADER-CONTENT_LENGTH'] = content_length_string.format(file_len)
        return file_content

def add_optional_headers():
    thread_local['RESPONSE_HEADERS'] = []
    for key, val in thread_local.items():
        if "HEADER-" in key:
            thread_local['RESPONSE_HEADERS'].append(val)
    thread_local['RESPONSE_HEADERS'] = ''.join(thread_local['RESPONSE_HEADERS'])

def create_response(resource=""):
    response_body = b""
    if resource != "":
        try:
            response_body = construct_body(resource)
        except Exception as e:
            print("Exception caught in response constructing:\n%s" % e.args)
    add_optional_headers()
    status = thread_local['RESPONSE_STATUS_CODE']
    response_line = create_resp_line(status)
    headers = construct_headers(status)

    return b"".join((response_line.encode(), headers.encode(), thread_local['RESPONSE_HEADERS'].encode(), http_server.new_line.encode(), response_body))




if __name__ == "__main__":
    tcp_server.main()