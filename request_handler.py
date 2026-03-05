import http_server, tcp_server

delimiter_line = "-----------------------------\n"
DEFAULT_FAILURE = 400
DEFAULT_SUCCESS = 200
NOT_IMPLEMENTED = 501
METHOD_NOT_SUPPORTED = 505

supported_methods = [
    "GET"
]

supported_headers = [
    "User-Agent",
    "Date",
    "Range,"
]


def handle_req_line(req_line):
    tokens = req_line.split(' ')
    if len(tokens) != 3:
        return DEFAULT_FAILURE

    if tokens[0] not in supported_methods:
        return NOT_IMPLEMENTED

    if tokens[2] != http_server.version:
        return METHOD_NOT_SUPPORTED

    print(
        "\nRequest method is %s\nTarget Resource is %s\n"
        % (tokens[0], tokens[1])
    )

    return DEFAULT_SUCCESS


def handle_headers(headers):
    status = DEFAULT_FAILURE
    has_body = False
    # print(delimiter_line + "Request headers:")
    for header in headers:
        try:
            field_name, value = header.split(': ')
        except Exception as e:
            print(e)
            return DEFAULT_FAILURE, has_body

        print("Used %s with value: %s" % (field_name, value))

        if field_name not in supported_headers:
            return DEFAULT_FAILURE, has_body

        status, has_body = handle_header(field_name, value)
        if status == DEFAULT_FAILURE:
            return DEFAULT_FAILURE, has_body

    return status, has_body


def handle_header(field, value):
    if field == "User-Agent":
        print("")
    elif field == "Range":
        print("")
    elif field == "Date":
        print("")
    else:
        return DEFAULT_FAILURE, False
    return DEFAULT_SUCCESS, False


def handle_body(body):
    print("Request included body: %s" % body)
    return DEFAULT_SUCCESS


def handle_request(request):
    body = ""
    req_parts = request.split("\r\n\r\n")
    if len(req_parts) != 2:
        body = "Request is malformed"
        return DEFAULT_FAILURE, body
    head_lines = req_parts[0].split("\r\n")

    print(delimiter_line + "LOG:")

    status = handle_req_line(head_lines[0])
    if status >= 300:
        return status, body

    status, has_body = handle_headers(head_lines[1::])
    if status >= 300:
        return status, body
    if has_body:
        status = handle_body(req_parts[1])
    return status, body


if __name__ == "__main__":
    tcp_server.main()