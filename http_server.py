import tcp_server, request_handler, response_constructor

new_line = "\r\n"
version = "HTTP/1.1"
status_codes= {
    200: "OK",
    206: "Partial Content",
    400: "Bad Request",
    404: "Not Found",
    416: "Range Not Satisfiable",
    500: "Internal Server Error",
    501: "Not Implemented",
    505: "HTTP Method Not Supported",
}

def request_processing(request):
    try:
        resource = request_handler.handle_request(request)

    except Exception as e:
        print("Exception caught:\n%s" % e.args)
        if len(e.args) == 1:
            request_handler.RESPONSE_STATUS_CODE = request_handler.DEFAULT_FAILURE
            return response_constructor.create_response(e.args)
        elif len(e.args) == 2:
            request_handler.RESPONSE_STATUS_CODE = e.args[0]
            return response_constructor.create_response(e.args[1])
        return response_constructor.create_response()

    request_handler.RESPONSE_STATUS_CODE = 200
    return response_constructor.create_response(resource)





if __name__ == "__main__":
    tcp_server.main()