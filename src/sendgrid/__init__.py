import json

import requests


class SendGridAPIError(Exception):
    
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class SendGridAPI(object):
    """API library to access the SendGrid REST API."""

    BASE_URL = 'https://sendgrid.com/api/'
    FORMAT = 'json'

    def __init__(self, api_user, api_key):
        self.api_user = api_user
        self.api_key = api_key

    def call(self, method, **kwargs):
        # newsletter api uses different url structure than other apis
        if method.startswith('newsletter'):
            api_method = method.replace('_', '/')
        else:
            api_method = method.replace('_', '.')

        url = '%s%s.%s' % (SendGridAPI.BASE_URL,
                           api_method,
                           SendGridAPI.FORMAT)
        kwargs.update({'api_user': self.api_user, 'api_key': self.api_key})

        result = json.loads(requests.get(url, kwargs).content)

        if 'error' in result:
            raise SendGridAPIError(result['error'])
        return result

    def __getattr__(self, method):
        def get(self, *args, **kwargs):
            return self.call(method, **kwargs)
        return get.__get__(self)
