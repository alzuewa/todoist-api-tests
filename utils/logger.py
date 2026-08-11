import json
import logging
import sys
from collections.abc import Callable
from functools import wraps

import allure
from allure_commons.types import AttachmentType
from requests.exceptions import JSONDecodeError

_logger = logging.getLogger(__name__)
console_formatter = logging.Formatter('\n==> {asctime} - [{levelname}] - {message}', style='{',
                                      datefmt='%Y-%m-%d %H:%M')
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel('INFO')
console_handler.setFormatter(console_formatter)
_logger.addHandler(console_handler)


def logger(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            allure.attach(
                body=json.dumps(result.json(), indent=4, ensure_ascii=True), name='Response',
                attachment_type=AttachmentType.JSON, extension='.json'
            )
        except JSONDecodeError:
            try:
                allure.attach(
                    body=result.text, name='Response', attachment_type=AttachmentType.TEXT, extension='.txt'
                )
            except JSONDecodeError:
                try:
                    allure.attach(
                        body=result.reason, name='Response', attachment_type=AttachmentType.TEXT, extension='.txt'
                    )
                except JSONDecodeError:
                    allure.attach(body='None', name="Response", attachment_type=AttachmentType.TEXT, extension=".txt")

        _logger.info(f'Request URL:: {result.request.url}')
        _logger.info(f'Request method:: {result.request.method}')
        _logger.info(f'Request headers:: {secure_headers(result.request.headers)}')
        if kwargs.get('json'):
            _logger.info(f'Request body:: {result.request.body.decode()}')
        else:
            _logger.info(f'Request body:: None')
        _logger.info(f'Response status code:: {result.status_code}')
        try:
            _logger.info(f'Response json:: {result.json()}\n<=====\n')
        except JSONDecodeError:
            try:
                _logger.info(f'Response text:: {result.text}\n<=====\n')
            except JSONDecodeError:
                try:
                    _logger.info(f'Response reason:: {result.reason}\n<=====\n')
                except JSONDecodeError:
                    _logger.info(f'Response body:: None\n<=====\n')
        return result

    return wrapper


def secure_headers(headers: dict):
    for key in headers:
        if key in ('Authorization', 'Cookie'):
            headers[key] = '*****'
    return headers
