import threading
import http_server, tcp_server, parser

# Constants
NO_RESPONSE_BODY = ""
SERVER_FAILURE = 500
BAD_REQUEST = 400
DEFAULT_SUCCESS = 200
NOT_IMPLEMENTED = 501
METHOD_NOT_SUPPORTED = 505
delimiter_line = "-----------------------------\n"

supported_methods = [
    "GET"
]

supported_headers = [
    "User-Agent",
    "Date",
    "Range,"
]

# Should be thread-local data
# REQUEST_UA_VALUE = ""
# REQUEST_RANGE_VALUE = None
# REQUEST_HAS_BODY = False
# REQUEST_DATE_VALUE = 0
# RESPONSE_STATUS_CODE = 200

thread_local = threading.current_thread().__dict__



def handle_req_line(req_line):
    tokens = req_line.split(' ')
    if len(tokens) != 3:
        thread_local['RESPONSE_STATUS_CODE'] = BAD_REQUEST
        raise Exception("BAD_REQUEST")

    if tokens[0] not in supported_methods:
        thread_local['RESPONSE_STATUS_CODE'] = NOT_IMPLEMENTED
        raise Exception("NOT_IMPLEMENTED")

    if tokens[2] != http_server.version:
        thread_local['RESPONSE_STATUS_CODE'] = METHOD_NOT_SUPPORTED
        raise Exception("METHOD_NOT_SUPPORTED")

    print(
        "\nRequest method is %s\nTarget Resource is %s\n"
        % (tokens[0], tokens[1])
    )
    resource = parser.target_parser(tokens[1])
    return resource



def handle_headers(headers):
    for header in headers:
        try:
            field_name, value = header.split(': ')
        except Exception as e:
            thread_local['RESPONSE_STATUS_CODE'] = BAD_REQUEST
            raise Exception("BAD_REQUEST")

        print("Used %s with value: %s" % (field_name, value))

        if field_name not in supported_headers:
            wrapper_handle_header(field_name, value)



def wrapper_handle_header(field, value):
    if field == "User-Agent":
        try:
            parser.user_agent_handler(value)
        except Exception as e:
            print("Error in User-Agent header parsing")
            raise e

    elif field == "Range":
        try:
            parser.range_handler(value)
        except Exception as e:
            print("Error in Range header parsing")
            raise e

    elif field == "Date":
        try:
            parser.date_handler(value)
        except Exception as e:
            print("Error in Date header parsing")
            raise e


def handle_body(body):
    print("Request included body: %s" % body)


def handle_request(request):
    req_parts = request.split("\r\n\r\n")
    if len(req_parts) != 2:
        thread_local['RESPONSE_STATUS_CODE'] = BAD_REQUEST
        raise Exception("BAD_REQUEST")

    head_lines = req_parts[0].split("\r\n")

    print(delimiter_line + "LOG:")
    resource = handle_req_line(head_lines[0])
    handle_headers(head_lines[1::])

    if "REQUEST_HAS_BODY" in thread_local.keys():
        handle_body(req_parts[1])
    return resource


if __name__ == "__main__":
    tcp_server.main()