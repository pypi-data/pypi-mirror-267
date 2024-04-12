from typing import TypeVar, overload

import yaml
from httpx import Client, Response
from pydantic import BaseModel

from ._log import LoggerBase
from ._util import wraps

T = TypeVar('T', bound=BaseModel)


class LinearClient(LoggerBase):
    """The main entrypoint to use LinearTest."""

    def __init__(self, test_client: Client):
        """
        Initialize the `LinearClient` instance.
        :param test_client: the Starlette TestClient instance
        """
        super().__init__()
        self.test_client = test_client

    def _log(self, prefix: str, dct: dict):
        for line in yaml.dump(dct).strip().split('\n'):
            print(prefix, line, sep='')

    @overload
    @wraps(Client.request)
    def request(self, *args, **kwargs) -> Response: ...

    @overload
    def request(self, method, url, *args, response_model: T, **kwargs) -> T: ...

    def request(
        self, method: str, url: str, *args, response_model: T | None = None, **kwargs
    ) -> T | Response:
        """Perform a request with request and response data logged."""
        # log the start of the request
        print(f' REQUEST START: {method} {url} '.center(self.logging_width, '-'))

        # log prefix
        prefix = '------+ '

        # log params
        if kwargs.get('params'):
            print('>>> Request params:')
            self._log(prefix, kwargs.get('params'))

        # log data
        if kwargs.get('data'):
            print('>>> Request data:')
            self._log(prefix, kwargs.get('data'))

        # log files
        if kwargs.get('files'):
            print('>>> Request files:')
            self._log(
                prefix, {key: file.name for key, file in kwargs.get('files').items()}
            )

        # log json
        if kwargs.get('json'):
            print('>>> Request JSON:')
            self._log(prefix, kwargs.get('json'))

        # log headers
        if kwargs.get('headers'):
            print('>>> Request headers:')
            self._log(prefix, kwargs.get('headers'))

        # log cookies
        if kwargs.get('cookies'):
            print('>>> Request cookies:')
            self._log(prefix, kwargs.get('cookies'))

        # use TestClient to perform the request
        response = self.test_client.request(method, url, *args, **kwargs)

        # return if not response model specified
        if response_model is None:
            print('<<< Response:', response.status_code, response.reason_phrase)
            print(f' REQUEST END: {method} {url} '.center(self.logging_width, '-'))

            return response

        # check if response is JSON
        content_type = response.headers.get('Content-Type')
        error_message = f'expected response type to be "application/json", got {content_type} instead.'
        assert content_type == 'application/json', error_message
        response_dict = response.json()

        # log response
        print('<<< Response JSON:')
        self._log(prefix, response_dict)

        # log the end of the request
        print(f' REQUEST END: {method} {url} '.center(self.logging_width, '-'))

        # parse the json dictionary to response_model
        return response_model.model_validate(response_dict)

    @overload
    @wraps(Client.get)
    def get(self, *args, **kwargs) -> Response: ...

    @overload
    def get(self, *args, response_model: T, **kwargs) -> T: ...

    def get(self, *args, response_model: T | None = None, **kwargs) -> T | Response:
        """Perform a GET request with request and response data logged."""
        return self.request('GET', *args, response_model=response_model, **kwargs)

    @overload
    @wraps(Client.post)
    def post(self, *args, **kwargs) -> Response: ...

    @overload
    def post(self, *args, response_model: T, **kwargs) -> T: ...

    def post(self, *args, response_model: T | None = None, **kwargs) -> T | Response:
        """Perform a POST request with request and response data logged."""
        return self.request('POST', *args, response_model=response_model, **kwargs)
