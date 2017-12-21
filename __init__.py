"""PytSite HTTP API Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from ._api import handle, endpoint, url, call, on_pre_request, on_request


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.t_js(__name__)
        assetman.js_module('http-api', __name__ + '@http-api')

    return assetman


def plugin_install():
    _register_assetman_resources().build(__name__)


def plugin_load():
    _register_assetman_resources()


def plugin_load_uwsgi():
    from pytsite import router, tpl
    from . import _eh, _controllers

    # HTTP API entry point route
    router.handle(_controllers.Entry, '/api/<int:http_api_version>/<path:http_api_endpoint>',
                  'pytsite.http_api@entry', methods='*')

    # Tpl globals
    tpl.register_global('http_api_endpoint', endpoint)

    # Event listeners
    router.on_response(_eh.router_response)
