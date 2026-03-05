import tcp_server, request_handler, response_constructor

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

def request_processing(request):
    return response_constructor.create_response(*request_handler.handle_request(request)).encode()





if __name__ == "__main__":
    tcp_server.main()