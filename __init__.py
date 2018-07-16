"""PytSite HTTP API Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import handle, endpoint, url, call, on_pre_request, on_request


def plugin_load():
    from plugins import assetman

    assetman.register_package(__name__)
    assetman.t_js(__name__, babelify=True)
    assetman.js_module('http-api', __name__ + '@http-api')


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)


def plugin_load_uwsgi():
    from pytsite import router, tpl
    from . import _controllers

    # HTTP API entry point route
    router.handle(_controllers.Entry, '/api/<path:http_api_endpoint>', 'http_api@entry', methods='*')

    # Tpl globals
    tpl.register_global('http_api_endpoint', endpoint)
