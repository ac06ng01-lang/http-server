import httpdate, threading, os, uritools
import request_handler, tcp_server

supported_range_units = [
    "bytes"
]

thread_local = threading.current_thread().__dict__


def user_agent_handler(value):
    thread_local['REQUEST_UA_VALUE'] = value


def range_handler(value):
    directives = value.split('=')
    if len(directives) != 2:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
        raise Exception("BAD_REQUEST")

    if directives[0] not in supported_range_units:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
        raise Exception("BAD_REQUEST")

    ranges = directives[1].split(',')
    if len(ranges) == 1:
        vals = ranges[0].split('-')
        print(vals)
        if vals[0] == '':
            if not vals[1].isnumeric():
                thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
                raise Exception("BAD_REQUEST")
            thread_local['REQUEST_RANGE_VALUE'] = int(vals[1]) * -1
            return

        elif vals[1] == '':
            if not vals[0].isnumeric():
                thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
                raise Exception("BAD_REQUEST")
            thread_local['REQUEST_RANGE_VALUE'] = int(vals[0])
            return

    thread_local['REQUEST_RANGE_VALUE'] = []
    print(ranges)
    for span in ranges:
        vals = span.split('-')
        if len(vals) != 2:
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
            raise Exception("BAD_REQUEST")

        if (not vals[0].isnumeric() or not vals[1].isnumeric()) or int(vals[0]) >= int(vals[1]):
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
            raise Exception("BAD_REQUEST")

        thread_local['REQUEST_RANGE_VALUE'].append([int(value) for value in vals],)


    if len(thread_local['REQUEST_RANGE_VALUE']) == 0:
        thread_local.pop('REQUEST_RANGE_VALUE')



def date_handler(value):
    try:
        thread_local['REQUEST_DATE_VALUE'] = httpdate.httpdate_to_unixtime(value)

    except ValueError as e:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
        raise Exception("Date value malformed")


def target_parser(target):
    file_name = "resources"
    uri_parts = uritools.urisplit(target)
    if uri_parts.isabsuri():
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
        raise Exception("BAD_REQUEST")
    elif uri_parts.isabspath():
        file_name += uri_parts.path
        # [print(ord(c)) for c in uri_parts.path]
        if uri_parts.path == '/':
            file_name += "index.html"

    file_name = os.path.normpath(file_name)

    print(file_name)
    if not file_name.startswith("resources") or not os.path.exists(file_name):
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.NOT_FOUND
        raise Exception("NOT_FOUND")

    return file_name



if __name__ == "__main__":
    tcp_server.main()