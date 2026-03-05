import http_server, tcp_server, request_handler


gen_headers = [
    "Server: Moshe\r\n",
    "Content-Type: text/html\r\n"
]


def create_resp_line(status):
    response_line = " ".join([http_server.version, str(status), http_server.status_codes[status], http_server.new_line])
    return response_line


def construct_headers(status):
    return "".join(gen_headers)


def construct_body(resource):
    ranges = request_handler.REQUEST_RANGE_VALUE
    if ranges is None or len(ranges) <= 0:
        ranges = 0
    return ""


def create_response(resource=""):
    status = request_handler.RESPONSE_STATUS_CODE
    response_line = create_resp_line(status)
    headers = construct_headers(status)
    response_body = construct_body(resource)
    return "".join([response_line, headers, http_server.new_line, response_body])




if __name__ == "__main__":
    tcp_server.main()