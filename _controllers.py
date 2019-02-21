"""PytSite HTTP API Endpoints
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router as _router, logger as _logger, lang as _lang, events as _events, routing as _routing, \
    http as _http, reg as _reg, errors as _errors
from . import _api


class Entry(_routing.Controller):
    def exec(self):
        del self.args['_pytsite_router_rule_name']
        endpoint = '/' + self.args.pop('http_api_endpoint')
        current_path = _router.current_path(False)
        request_method = _router.request().method

        # Switch language
        language = _router.request().headers.get('Accept-Language')  # type: str
        if language:
            for lng in language.split(','):
                lng = lng.strip()
                if not lng.startswith('q=') and _lang.is_defined(language):
                    _lang.set_current(language)
                    break
        try:
            _events.fire('http_api@pre_request')
            rule = _api.match(_router.request().method, endpoint)
            _events.fire('http_api@request')

            controller = rule.controller_class()  # type: _routing.Controller
            controller.request = self.request
            controller.args.update(self.args)
            controller.args.update(rule.args)
            controller.args['_pytsite_http_api_rule_name'] = rule.name
            controller.args.validate()

            response = controller.exec()
            return response if isinstance(response, _http.Response) else _http.JSONResponse(response)

        except (_http.error.Base, _errors.ForbidOperation) as e:
            if _reg.get('debug'):
                _logger.error(e)
            else:
                _logger.error('{} {}: {}'.format(request_method, current_path, e.description))

            if isinstance(e, _errors.ForbidOperation):
                e = _http.error.Forbidden(e)

            if e.response and isinstance(e.response, _http.JSONResponse):
                response = e.response
                response.status_code = e.code
            else:
                # It is important to do `str(e.description)`, because `e.description` might be an exception
                response = _http.JSONResponse({'error': str(e.description)}, e.code)

            return response

        except UserWarning as e:
            _logger.warn('{} {}: {}'.format(request_method, current_path, e))
            return _http.JSONResponse({'warning': str(e)}, e.args[1] if len(e.args) > 1 else 500)

        except Exception as e:
            _logger.error('{} {}: {}'.format(request_method, current_path, e), exc_info=e)
            return _http.JSONResponse({'error': str(e)}, e.args[1] if len(e.args) > 1 else 500)
