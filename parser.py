import http_server, request_handler

supported_range_units = [
    "bytes"
]


def user_agent_handler(value):
    request_handler.REQUEST_UA_VALUE = value


def range_handler(value):
    directives = value.split(':')
    if len(directives) != 2:
        raise Exception(request_handler.DEFAULT_FAILURE)

    if directives[0] not in supported_range_units:
        raise Exception(request_handler.DEFAULT_FAILURE)

    ranges = directives[1].split(',')
    request_handler.REQUEST_RANGE_VALUE = []
    for span in ranges:
        vals = span.split('-')
        if len(vals) != 2:
            raise Exception(request_handler.DEFAULT_FAILURE)

        if not vals[0].isnumeric() or vals[1].isnumric():
            raise Exception(request_handler.DEFAULT_FAILURE)

        request_handler.REQUEST_RANGE_VALUE.append(span)

    if len(request_handler.REQUEST_RANGE_VALUE) == 0:
        request_handler.REQUEST_RANGE_VALUE = None



def date_handler(value):
    request_handler.REQUEST_DATE_VALUE = value


def target_parser(target):
    pass