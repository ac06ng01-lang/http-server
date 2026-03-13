import threading, httpdate, time, mimetypes, os.path
from filelock import FileLock
import http_server, tcp_server, request_handler

gen_headers = [
    "Server: Moshe\r\n",
    "Connection: close\r\n",
]


boundary_string = "SEPARATING_STRING"
multipart_content_type_value = "multipart/byteranges; boundary=" + boundary_string
last_modified_string = "Last-Modified: {0}\r\n"
content_length_string = "Content-Length: {0}\r\n"
date_string = "Date: {0}\r\n"
multipart_prefix_string = "--"+ boundary_string + "\r\n{0}{1}"
content_range_string = "Content-Range: bytes {0}-{1}/{2}\r\n"
content_type_string = "Content-Type: {0}\r\n"

thread_local = threading.current_thread().__dict__

def create_resp_line(status):
    response_line = " ".join([http_server.version, str(status), http_server.status_codes[status], http_server.new_line])
    return response_line

def construct_headers():
    thread_local['HEADER-DATE'] = date_string.format(httpdate.unixtime_to_httpdate(int(time.time())))
    return "".join(gen_headers)

def get_content_type(resource):
    return mimetypes.guess_type(resource)[0] or "text/html"


def construct_body(resource):
    try:
        with FileLock(resource + ".lock", thread_local=False):
            with open(resource, 'rb') as f:
                file_content = f.read()
    except OSError as e:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.NOT_FOUND
        raise Exception("NOT_FOUND")

    content_type = content_type_string.format(get_content_type(resource))
    file_len = len(file_content)

    thread_local['HEADER-CONTENT_TYPE'] = content_type
    thread_local['HEADER-LAST_MODIFIED'] = last_modified_string.format(httpdate.unixtime_to_httpdate(
        int(os.path.getmtime(resource))))

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
                    partial_content += multipart_prefix_string.format(content_type,
                           content_range_string.format(range_start, range_end, file_len,),).encode()
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
    headers = []
    for key, val in thread_local.items():
        if "HEADER-" in key:
            headers.append(val)
    return ''.join(headers)

def create_response(resource=""):
    status = thread_local['RESPONSE_STATUS_CODE']
    response_body = b""
    if resource != "":
        if status == request_handler.NOT_MODIFIED:
            thread_local['HEADER-LAST_MODIFIED'] = last_modified_string.format(
                httpdate.unixtime_to_httpdate(int(os.path.getmtime(resource)))
            )
        try:
            response_body = construct_body(resource)
        except Exception as e:
            print("Exception caught in response constructing:\n%s" % e.args)
    headers = construct_headers()
    headers += add_optional_headers()
    # updating in case it changed in any of the former functions
    status = thread_local['RESPONSE_STATUS_CODE']
    response_line = create_resp_line(status)


    return b"".join((response_line.encode(), headers.encode(), http_server.new_line.encode(), response_body))




if __name__ == "__main__":
    tcp_server.main()