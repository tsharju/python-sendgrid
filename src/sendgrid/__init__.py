import json

import requests


class SendGridAPIError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class SendGridAPI(object):
    """API library to access the SendGrid REST API."""

    API_PROTOCOL = 'https'
    API_DOMAIN = 'sendgrid.com'
    FORMAT = 'json'

    def __init__(self, api_user, api_key):
        self.api_user = api_user
        self.api_key = api_key

    def call(self, method, **kwargs):
        # newsletter api uses different url structure than other apis
        if method.startswith('api_newsletter'):
            api_method = method.replace('_', '/')
        else:
            api_method = method.replace('_', '.')

        url = '%s://%s/%s.%s' % (SendGridAPI.API_PROTOCOL,
                                 SendGridAPI.API_DOMAIN,
                                 api_method,
                                 SendGridAPI.FORMAT)
        kwargs.update({'api_user': self.api_user, 'api_key': self.api_key})

        result = json.loads(requests.get(url, params=kwargs).content)

        if 'error' in result:
            raise SendGridAPIError(result['error'])
        return result

    def newsletter_add(self, identity, name, subject, text, html):
        """Create a new Newsletter."""
        self.api_newsletter_add(identity=identity, name=name,
                                subject=subject, text=text, html=html)

    def newsletter_edit(self, name, newname, identity, subject, text, html):
        """Edit an existing Newsletter."""
        self.api_newsletter_edit(name=name, newname=newname, identity=identity,
                                 subject=subject, text=text, html=html)

    def newsletter_get(self, name):
        """Retrieve the contents of an existing Newsletter."""
        return self.api_newsletter_get(name=name)

    def newsletter_list(self, name=""):
        """Retrieve a list of all existing Newsletters."""
        return self.api_newsletter_list(name=name)

    def newsletter_delete(self, name):
        """Remove an existing Newsletter."""
        return self.api_newsletter_delete(name=name)

    def newsletter_lists_add(self, list, name=""):
        """Create a new Recipient List."""
        return self.api_newsletter_lists_add(list=list, name=name)

    def newsletter_lists_edit(self, list, newlist):
        """Rename a Recipient List."""
        return self.api_newsletter_lists_edit(list=list, newlist=newlist)

    def newsletter_lists_get(self, list=""):
        """List all Recipient Lists on your account, or check if a particular
        List exists."""
        return self.api_newsletter_lists_get(list=list)

    def newsletter_lists_delete(self, list):
        """Remove a Recipient List from your account."""
        return self.api_newsletter_lists_delete(list=list)

    def newsletter_lists_email_add(self, list, data):
        """Add one or more emails to a Recipient List."""
        if type(data) == type(dict):
            data = json.dumps(data)
        return self.api_newsletter_lists_email_add(list=list, data=data)

    def newsletter_lists_email_get(self, list, email=""):
        """Get the email addresses and associated fields for a
        Recipient list."""
        return self.api_newsletter_lists_email_get(list=list, email=email)

    def newsletter_lists_email_delete(self, list, email):
        """Remove one or more emails from a Recipient List."""
        return self.api_newsletter_lists_email_delete(list=list, email=email)

    def newsletter_recipients_add(self, name, list):
        """Add Recipient Lists to a Newsletter."""
        return self.api_newsletter_recipients_add(name=name, list=list)

    def newsletter_recipients_get(self, name):
        """Retrieve the Recipient Lists attached to an existing Newsletter."""
        return self.api_newsletter_recipients_get(name=name)

    def newsletter_recipients_delete(self, name, list):
        """Delete Recipient Lists from a Newsletter."""
        return self.api_newsletter_recipients_delete(name=name, list=list)

    def newsletter_schedule_add(self, name, at="", after=""):
        """Schedule a delivery time for an existing Newsletter."""
        return self.api_newsletter_schedule_add(name=name, at=at, after=after)

    def newsletter_schedule_get(self, name):
        """Retrieve the scheduled delivery time for and existing Newsletter."""
        return self.api_newsletter_schedule_get(name=name)

    def newsletter_schedule_delete(self, name):
        """Cancel a scheduled send for a Newsletter."""
        return self.api_newsletter_schedule_delete(name)

    def __getattr__(self, method):
        def get(self, *args, **kwargs):
            return self.call(method, **kwargs)
        return get.__get__(self)
