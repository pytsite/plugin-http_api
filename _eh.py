"""PytSite HTTP API Event Handlers.
"""
from pytsite import http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_response(response: _http.Response):
    # No cookies in responses from HTTP API
    if 'PytSite-HTTP-API-Version' in response.headers:
        response.headers.remove('Set-Cookie')
