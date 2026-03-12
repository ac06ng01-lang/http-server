import threading
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

thread_local = threading.current_thread().__dict__

def request_processing(request):
    try:
        resource = request_handler.handle_request(request)

    except Exception as e:
        print("Exception caught in request handling:\n%s" % e.args)
        if not 'RESPONSE_STATUS_CODE' in thread_local.keys():
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.SERVER_FAILURE
        # if request_handler.RESPONSE_STATUS_CODE == DEFAULT_SUCCESS:
        #     request_handler.RESPONSE_STATUS_CODE = SERVER_FAILURE
        # if len(e.args) == 1:
        #     request_handler.RESPONSE_STATUS_CODE = request_handler.DEFAULT_FAILURE
        #     return response_constructor.create_response(e.args)
        # elif len(e.args) == 2:
        #     request_handler.RESPONSE_STATUS_CODE = e.args[0]
        #     return response_constructor.create_response(e.args[1])
        # request_handler.RESPONSE_STATUS_CODE = request_handler.SERVER_FAILURE
        return response_constructor.create_response()

    thread_local['RESPONSE_STATUS_CODE'] = request_handler.DEFAULT_SUCCESS
    return response_constructor.create_response(resource)





if __name__ == "__main__":
    tcp_server.main()