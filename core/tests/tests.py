import time
from unittest import skip

from django.urls import reverse
from rest_framework import status

from core.tests import MyAPITestCase, response_to_json, json_pretty_print
from rbroker.settings import TASK_EXECUTION_TIME


class ApiTestCase(MyAPITestCase):

    fixtures = ['data.json']

# python manage.py test core.tests.tests.ApiTestCase.test_task_list
    def test_task_list(self):
        url = reverse('tasks-list')
        response = self.client.get(url, format='json')
        content = response_to_json(response)

        print(json_pretty_print(content))
        self.assertEqual(len(content), 1)


# python manage.py test core.tests.tests.ApiTestCase.test_task_begin
    def test_task_begin(self):
        DEVICE_ID = 1
        TASK_ID = 1
        task = {
            "device": DEVICE_ID
        }

        url = reverse('begin', kwargs=dict(pk=TASK_ID))
        print(url)
        response = self.client.put(url, data=task, format='json')

        content = response_to_json(response)
        print(json_pretty_print(content))

# python manage.py test core.tests.tests.ApiTestCase.test_task_success
    def test_task_success(self):
        DEVICE_ID = 1
        TASK_ID = 2
        task = {
            "device": DEVICE_ID
        }

        url = reverse('success', kwargs=dict(pk=TASK_ID))
        print(url)
        response = self.client.put(url, data=task, format='json')

        content = response_to_json(response)
        print(json_pretty_print(content))

# python manage.py test core.tests.tests.ApiTestCase.test_task_failure
    def test_task_failure(self):
        DEVICE_ID = 1
        TASK_ID = 2
        task = {
            "device": DEVICE_ID
        }

        url = reverse('failure', kwargs=dict(pk=TASK_ID))
        print(url)
        response = self.client.put(url, data=task, format='json')

        content = response_to_json(response)
        print(json_pretty_print(content))


# python manage.py test core.tests.tests.ApiTestCase.test_task_timeout
    @skip('Skipped since testunit uses a different database connection than django_q, unfortunately (temporary) '
          'switched to manual testing of the feature')
    def test_task_timeout(self):
        DEVICE_ID = 1
        TASK_ID = 1
        task = {
            "device": DEVICE_ID
        }

        url = reverse('begin', kwargs=dict(pk=TASK_ID))
        # print(url)
        response = self.client.put(url, data=task, format='json')

        content = response_to_json(response)
        print(json_pretty_print(content))

        time.sleep(TASK_EXECUTION_TIME*2)

        url = reverse('success', kwargs=dict(pk=TASK_ID))
        print(url)
        response = self.client.put(url, data=task, format='json')

        content = response_to_json(response)
        print(json_pretty_print(content))

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
