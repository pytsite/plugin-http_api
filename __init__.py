"""PytSite HTTP API Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from ._api import handle, endpoint, url, call, on_pre_request, on_request


def plugin_load():
    from pytsite import router, tpl
    from plugins import assetman
    from . import _eh, _controllers

    # HTTP entry point route
    router.handle(_controllers.Entry, '/api/<int:http_api_version>/<path:http_api_endpoint>',
                  'pytsite.http_api@entry', methods='*')

    # Tpl globals
    tpl.register_global('http_api_endpoint', endpoint)

    # Event listeners
    router.on_response(_eh.router_response)

    # Assets
    assetman.register_package(__name__)
    assetman.t_js(__name__)
    assetman.js_module('http-api', __name__ + '@http-api')
