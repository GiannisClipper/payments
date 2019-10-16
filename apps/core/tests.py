from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

import json

from apps.settings import JWTOKEN_PREFIX


class APITests:

    namespace = None

    def api_request(
        self, url, method='GET', args=None, payload=None, token=None
    ):

        if token:
            self.client.credentials(
                HTTP_AUTHORIZATION=f'{JWTOKEN_PREFIX} {token}'
            )

        if self.namespace:
            payload = {self.namespace: payload}

        payload = json.dumps(payload)

        content_type = 'application/json'

        if method == 'POST':
            res = self.client.post(url, payload, content_type=content_type)
        elif method == 'PATCH':
            res = self.client.patch(url, payload, content_type=content_type)
        elif method == 'DELETE':
            res = self.client.delete(url, payload, content_type=content_type)
        else:  # GET
            res = self.client.get(url, content_type=content_type)

        res.data = json.loads(res.data)

        return res

    def create_user(self, **sample):
        return get_user_model().objects.create_user(**sample)

    def create_admin(self, **sample):
        return get_user_model().objects.create_superuser(**sample)

    def setUp(self):

        self.client = APIClient()
