import tcp_server

new_line = "\r\n"
version = "HTTP/1.1"
status_codes= {
    200: "OK",
    400: "Bad Request",
    404: "Not Found"
}


def create_resp_line(status):
    response_line = " ".join([version, status, status_codes[status], new_line])
    return response_line



def create_response(status):
    response_line = create_resp_line(status)    #"HTTP/1.1 404 Not Found\r\n"
    headers = "".join([
        "Server: Moshe\r\n"
        "Content-Type: text/html\r\n"
    ])
    response_body = ""
    return "".join([response_line, headers, "\r\n", response_body])




def handle_request(data):
    print(data)



    return create_response(data).encode()



if __name__ == "__main__":
    tcp_server.main()