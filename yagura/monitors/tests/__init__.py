from urllib.error import HTTPError, URLError

from django.utils.six import StringIO


def mocked_urlopen(*args, **kwargs):
    class MockResponse(object):
        def __init__(self, status_code):
            self.code = status_code

    url = args[0]
    if url[-3:] == '200':
        return MockResponse(200)
    raise HTTPError(url=url, code=404, msg='Failure', hdrs='', fp=StringIO())


def mocked_urlopen_urlerror(message='Error'):
    def _mocked_url_urlerror(*args, **kwargs):
        raise URLError(reason=message)
    return _mocked_url_urlerror
