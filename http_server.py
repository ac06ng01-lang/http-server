import threading
import tcp_server, request_handler, response_constructor, caching_handler

new_line = "\r\n"
version = "HTTP/1.1"
status_codes= {
    200: "OK",
    206: "Partial Content",
    304: "Not Modified",
    400: "Bad Request",
    404: "Not Found",
    412: "Precondition Failed",
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
        return response_constructor.create_response()

    if 'REQUEST_MODIFIED_SINCE' in thread_local.keys():
        try:
            caching_handler.modified_since_resolver(resource)
        except Exception as e:
            if e.args[0] == request_handler.NOT_MODIFIED:
                return response_constructor.create_response()


    if 'REQUEST_UNMODIFIED_SINCE' in thread_local.keys():
        try:
            caching_handler.unmodified_since_resolver(resource)
        except Exception as e:
            if e.args[0] == request_handler.PRECONDITION_FAILED:
                return response_constructor.create_response()


    try:
        cached_response = caching_handler.fetch_from_cache(resource)
        return cached_response
    except FileNotFoundError as error:
        print(f"finding in cached failed!\nthe error is {error}")
        if not 'RESPONSE_STATUS_CODE' in thread_local.keys():
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.DEFAULT_SUCCESS
        return response_constructor.create_response(resource)
    except Exception as e:
        print(f"finding in cached failed!\nerror is {e}")
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.SERVER_FAILURE
        return response_constructor.create_response()




if __name__ == "__main__":
    tcp_server.main()