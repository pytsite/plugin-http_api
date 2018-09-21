"""PytSite HTTP API Endpoints
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router as _router, logger as _logger, lang as _lang, events as _events, routing as _routing, \
    http as _http, reg as _reg
from . import _api


class Entry(_routing.Controller):
    def exec(self):
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

            status = 200
            controller = rule.controller_class()  # type: _routing.Controller
            controller.request = self.request
            controller.args.update(self.args)
            controller.args.update(rule.args)
            controller.args['_pytsite_http_api_rule_name'] = rule.name
            controller.args.validate()
            controller_response = controller.exec()

            if isinstance(controller_response, _http.Response):
                return controller_response

            if isinstance(controller_response, tuple):
                if len(controller_response) > 1:
                    body, status = controller_response[0], controller_response[1]
                else:
                    body = controller_response[0]
            else:
                body = controller_response

            # Simple string should be returned as text/html
            if isinstance(body, str):
                response = _http.Response(body, status, mimetype='text/html')
            else:
                if isinstance(body, _routing.ControllerArgs):
                    body = dict(body)

                response = _http.JSONResponse(body, status)

            return response

        except _http.error.Base as e:
            log_msg = '{} {}: {}'.format(request_method, current_path, e.description)

            if _reg.get('debug'):
                _logger.error(log_msg, exc_info=e)
            else:
                _logger.error(log_msg)

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
