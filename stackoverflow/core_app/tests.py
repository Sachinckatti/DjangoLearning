from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from core_app.views import AnswerView
# Create your tests here.

class TestAnswerView(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = AnswerView.as_view({'get': 'list'})
        self.url = '/answer/'

    def test_list(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_list_api(self):
        self.client = APIClient()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))