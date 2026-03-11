import httpdate, threading
import http_server, request_handler

supported_range_units = [
    "bytes"
]

thread_local = threading.current_thread().__dict__


def user_agent_handler(value):
    thread_local['REQUEST_UA_VALUE'] = value


def range_handler(value):
    directives = value.split(':')
    if len(directives) != 2:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
        raise Exception("BAD_REQUEST")

    if directives[0] not in supported_range_units:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
        raise Exception("BAD_REQUEST")

    ranges = directives[1].split(',')
    thread_local['REQUEST_RANGE_VALUE'] = []
    for span in ranges:
        vals = span.split('-')
        if len(vals) != 2:
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
            raise Exception("BAD_REQUEST")

        if not vals[0].isnumeric() or vals[1].isnumric():
            thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
            raise Exception("BAD_REQUEST")

        thread_local['REQUEST_RANGE_VALUE'].append(span)


    if len(thread_local['REQUEST_RANGE_VALUE']) == 0:
        thread_local.pop('REQUEST_RANGE_VALUE')



def date_handler(value):
    try:
        thread_local['REQUEST_DATE_VALUE'] = httpdate.httpdate_to_unixtime(value)

    except ValueError as e:
        thread_local['RESPONSE_STATUS_CODE'] = request_handler.BAD_REQUEST
        raise Exception("Date value malformed")


def target_parser(target):
    pass