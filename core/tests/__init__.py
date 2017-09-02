# Create your tests here.
import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


def response_to_json(response):
    """ Transforms the content of a response into a python dictionary
    """
    # Because http returns bytes, no strings, we need to parse the content
    if response.status_code != status.HTTP_204_NO_CONTENT:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception(response.status_code)


def json_pretty_print(to_print):
    return json.dumps(to_print, indent=4, sort_keys=True)


class MyAPITestCase(APITestCase):

    def setUp(self):
        username = 'admin'
        password = 'adminadmin'
        self.client = APIClient()
        self.client.login(username=username, password=password)

        # self.user = User.objects.get(username=username)
        # self.factory = APIRequestFactory()

    def tearDown(self):
        self.client.logout()
