import requests

class VKApi(object):
    """..."""

    api_url = 'https://api.vk.com/method/'

    def __init__(self, token, v=5.68, proxies=False):
        """..."""
        self.token = token
        self.version = v
        self.proxies = proxies

        self.messages = Messages(self)
        self.groups = Groups(self)
        self.users = Users(self)

    def make_request(self, method, params):
        """..."""
        params.update({
           'access_token': self.token,
           'v': self.version
        })
        url = '{url}{method}'.format(
            url=self.api_url,
            method=method
        )
        if self.proxies:
            request = requests.get(
                url,
                params=params,
                proxies=self.proxies
            )
        else:
            request = requests.get(
                url,
                params=params
            )

        return request.json()


class APIBranch(object):
    """..."""

    def __init__(self, api_obj):
        self.api = api_obj


class Users(APIBranch):
    """..."""

    def get(self, user_ids, fields='first_name, last_name', name_case='nom'):
        """..."""

        return self.api.make_request('users.get', {
            'user_ids': user_ids,
            'fields': fields,
            'name_case': name_case
        })


class Messages(APIBranch):
    """..."""

    def send(self, user_id, message):
        """..."""
        return self.api.make_request('messages.send', {
            'user_id': user_id,
            'message': message
        })


class Groups(APIBranch):
    """..."""


    def get(self, user_id, filter, count=1000):
        """..."""
        return self.api.make_request('groups.get', {
            'user_id': user_id,
            'filter': filter,
            'count': count
        })

    def get_by_id(self, id, fields=False):
        """..."""
        return self.api.make_request('groups.getById', {
            'group_id': id
        })

    def get_callback_servers(self, group_id):
        """..."""
        return self.api.make_request('groups.getCallbackServers', {
            'group_id': group_id
        })

    def add_callback_server(self, group_id, name, url, secret):
        """..."""
        return self.api.make_request('groups.addCallbackServer', {
            'group_id': group_id,
            'url': url,
            'title': name,
            'secret_key': secret
        })

    def set_callback_settings(self, group_id, server_id, params=dict()):
        """..."""
        params.update({
            'server_id': server_id,
            'group_id': group_id
        })
        return self.api.make_request('groups.setCallbackSettings',
            params
        )

    def get_callback_confirmation_code(self, group_id):
        """..."""
        return self.api.make_request('groups.getCallbackConfirmationCode', {
            'group_id': group_id
        })

