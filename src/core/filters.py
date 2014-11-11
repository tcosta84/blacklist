from log_request_id.filters import RequestIDFilter
from log_request_id import local


class ExtraRequestFilter(RequestIDFilter):
    def filter(self, record):
        record.remote_addr = getattr(local, 'remote_addr', None)
        return RequestIDFilter.filter(self, record)
