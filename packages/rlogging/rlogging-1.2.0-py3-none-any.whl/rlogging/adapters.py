import logging
import uuid
from typing import Any, Dict, Optional, Tuple


class RLoggerAdapter(logging.LoggerAdapter):
    """Адаптер над логгером

    Позволяет логировать с передачей котекста

    """

    flow_id: uuid.UUID

    def __init__(self, logger: logging.Logger, extra: Optional[Dict[str, Any]] = None) -> None:
        extra = extra if extra is not None else {}

        super().__init__(logger, extra)

        self.flow_id = uuid.uuid1()

    def _extra_update(self, kwargs: Dict[str, Any], extra: Dict[str, Any]):
        extra = extra.copy()

        extra.update(kwargs.get('extra', {}))

        kwargs['extra'] = extra

    def process(self, msg: Any, kwargs: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        kwargs.setdefault('stacklevel', 2)

        extra = {
            'flow_id': self.flow_id,
        }

        self._extra_update(kwargs, extra)
        self._extra_update(kwargs, self.extra)

        return msg, kwargs


class AppLoggerAdapter(RLoggerAdapter):
    pass


class HttpLoggerAdapter(AppLoggerAdapter):
    """Флоу для логирования веб запросов/ответов"""

    def request(
        self,
        url: str,
        method: str,
        *args,
        **kwargs,
    ):
        kwargs.setdefault('stacklevel', 3)

        extra = {
            'http': {
                'url': url,
                'method': method,
            }
        }
        self._extra_update(kwargs, extra)

        self.info('http request', **kwargs)

    def response(self, code: int, *args, **kwargs):
        kwargs.setdefault('stacklevel', 3)

        extra = {
            'http': {
                'code': code,
            },
        }
        self._extra_update(kwargs, extra)

        self.info('http response', **kwargs)
