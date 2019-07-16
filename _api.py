"""PytSite HTTP API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union, Mapping, Type, Tuple
from pytsite import router, http, routing, events

_rules_map = routing.RulesMap()


def handle(method: Union[str, Tuple[str, ...]], path: str, controller: Union[str, Type[routing.Controller]],
           name: str = None, defaults: dict = None):
    """Register API request handler
    """
    if isinstance(controller, str):
        controller = _rules_map.get(controller).controller_class

    _rules_map.add(routing.Rule(controller, path, name, defaults, method))


def match(method: str, path: str) -> routing.Rule:
    try:
        return _rules_map.match(path, method)[0]
    except routing.error.RuleNotFound:
        raise http.error.NotFound()


def endpoint(name: str, args: Mapping = None) -> str:
    """Get HTTP API rule's endpoint
    """
    return _rules_map.path(name, args).lstrip('/')


def url(name: str, args: Mapping = None) -> str:
    """Get an URL for an HTTP API endpoint
    """
    return router.rule_url('http_api@entry', {
        'http_api_endpoint': _rules_map.path(name, args).lstrip('/')
    })


def call(name: str, args: Mapping = None):
    """Call a controller
    """
    controller = _rules_map.get(name).controller_class()  # type: routing.Controller
    controller.args.update(args)
    controller.args.validate()

    return controller.exec()


def on_pre_request(handler, priority: int = 0):
    """Register handler which will be called before handling every request to HTTP API.
    """
    events.listen('http_api@pre_request', handler, priority)


def on_request(handler, priority: int = 0):
    """Register handler which will be called on every request to HTTP API.
    """
    events.listen('http_api@request', handler, priority)
