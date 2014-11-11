import time
import logging

from log_request_id.middleware import RequestIDMiddleware
from log_request_id import local


logger = logging.getLogger(__name__)

HR = '-' * 40


class ExtraRequestMiddleware(RequestIDMiddleware):
    def process_request(self, request):
        local.start_time = time.time()
        RequestIDMiddleware.process_request(self, request)
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']
        local.remote_addr = request.META['REMOTE_ADDR']

        logger.info(HR)
        logger.info('BEGIN TRANSACTION')
        logger.info(HR)
        logger.info('request.user: %s' % request.user)
        logger.info('request.method: %s' % request.method)
        logger.info('request.path: %s' % request.path)
        logger.debug('request.body: %s' % request.body)

    def process_response(self, request, response):
        try:
            elapsed = time.time() - local.start_time
            logger.info('response.status_code: %s' % response.status_code)
            logger.debug('response: %s' % response)
            logger.info(HR)
            logger.info('END TRANSACTION - %.6f second(s)' % elapsed)
            logger.info(HR)
        except:
            pass
        return response
