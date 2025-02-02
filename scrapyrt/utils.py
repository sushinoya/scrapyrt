import inspect

from scrapy import Request
from scrapy_selenium import SeleniumRequest


def extract_scrapy_request_args(dictionary, raise_error=False):
    """
    :param dictionary: Dictionary with parameters passed to API
    :param raise_error: raise ValueError if key is not valid arg for
                        scrapy.http.Request
    :return: dictionary of valid scrapy.http.Request positional and keyword
            arguments.
    """
    result = dictionary.copy()
    request_args = inspect.getfullargspec(Request.__init__).args
    selenium_request_args = inspect.getfullargspec(SeleniumRequest.__init__).args
    all_valid_args = request_args + selenium_request_args
    for key in dictionary.keys():
        if key not in all_valid_args:
            result.pop(key)
            if raise_error:
                msg = u"{!r} is not a valid argument for scrapy.SeleniumRequest.__init__"
                raise ValueError(msg.format(key))
    return result


try:
    from scrapy.utils.python import to_bytes
except ImportError:
    def to_bytes(text, encoding=None, errors='strict'):
        """Return the binary representation of `text`. If `text`
        is already a bytes object, return it as-is."""
        if isinstance(text, bytes):
            return text
        if not isinstance(text, str):
            raise TypeError('to_bytes must receive a unicode, str or bytes '
                            'object, got %s' % type(text).__name__)
        if encoding is None:
            encoding = 'utf-8'
        return text.encode(encoding, errors)
