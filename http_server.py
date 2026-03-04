import tcp_server

new_line = "\r\n"
version = "HTTP/1.1"
status_codes= {
    200: "OK",
    206: "Partial Content",
    400: "Bad Request",
    404: "Not Found",
    416: "Range Not Satisfiable",
    501: "Not Implemented",
    505: "HTTP Method Not Supported",
}

gen_headers = [
    "Server: Moshe\r\n",
    "Content-Type: text/html\r\n"
]

supported_methods = [
    "GET"
]

supported_headers = [
    "User-Agent",
    "Date",
    "Range,"
]

def create_resp_line(status):
    response_line = " ".join([version, str(status), status_codes[status], new_line])
    return response_line


def construct_headers(status):
    return "".join(gen_headers)


def construct_body(status):
    return ""


def create_response(status):
    response_line = create_resp_line(status)    #"HTTP/1.1 404 Not Found\r\n"
    headers = construct_headers(status)
    response_body = construct_body(status)
    return "".join([response_line, headers, new_line, response_body])


def handle_req_line(req_line):
    tokens = req_line.split(' ')
    if len(tokens) != 3:
        return 400

    if tokens[0] not in supported_methods:
        return 501

    if tokens[2] != version:
        return 505

    return 200


def handle_headers(headers):
    status = 400
    body = False
    for header in headers:
        try:
            field_name, value = header.split(': ')
        except Exception as e:
            print(e)
            return status, body
        if field_name not in supported_headers:
            return status, body
        print()

    return status, body


def handle_body(body):
    return 200

def handle_request(request):
    print(request)
    status = 400
    req_parts = request.split("\r\n\r\n")
    print(req_parts)
    if len(req_parts) != 2:
        print(1)
        return create_response(status).encode()
    head_lines = req_parts[0].split("\r\n")
    status = handle_req_line(head_lines[0])
    if status >= 300:
        print(2)
        return create_response(status).encode()

    status, has_body = handle_headers(head_lines[1::])
    if status >= 300:
        print(3)
        return create_response(status).encode()
    if has_body:
        status = handle_body(req_parts[1])
    return create_response(status).encode()



if __name__ == "__main__":
    tcp_server.main()