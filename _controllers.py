"""PytSite HTTP API Endpoints
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router, logger, lang, events, routing, http, reg, errors
from . import _api


class Entry(routing.Controller):
    def exec(self):
        del self.args['_pytsite_router_rule_name']
        endpoint = '/' + self.args.pop('http_api_endpoint')
        current_path = router.current_path(False)
        request_method = router.request().method

        # Switch language
        language = router.request().headers.get('Accept-Language')  # type: str
        if language:
            for lng in language.split(','):
                lng = lng.strip()
                if not lng.startswith('q=') and lang.is_defined(language):
                    lang.set_current(language)
                    break
        try:
            events.fire('http_api@pre_request')
            rule = _api.match(router.request().method, endpoint)
            events.fire('http_api@request')

            controller = rule.controller_class()  # type: routing.Controller
            controller.request = self.request
            controller.args.update(self.args)
            controller.args.update(rule.args)
            controller.args['_pytsite_http_api_rule_name'] = rule.name
            controller.args.validate()

            response = controller.exec()
            return response if isinstance(response, http.Response) else http.JSONResponse(response)

        except (http.error.Base, errors.ForbidOperation) as e:
            if reg.get('debug'):
                logger.error(e)
            else:
                logger.error('{} {}: {}'.format(request_method, current_path, e.description))

            if isinstance(e, errors.ForbidOperation):
                e = http.error.Forbidden(e)

            if e.response and isinstance(e.response, http.JSONResponse):
                response = e.response
                response.status_code = e.code
            else:
                # It is important to do `str(e.description)`, because `e.description` might be an exception
                response = http.JSONResponse({'error': str(e.description)}, e.code)

            return response

        except UserWarning as e:
            logger.warn('{} {}: {}'.format(request_method, current_path, e))
            return http.JSONResponse({'warning': str(e)}, 200)

        except Exception as e:
            logger.error('{} {}: {}'.format(request_method, current_path, e), exc_info=e)
            return http.JSONResponse({'error': str(e)}, 500)
