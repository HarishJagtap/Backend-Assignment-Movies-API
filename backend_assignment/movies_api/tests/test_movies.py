from django.test import TestCase
from rest_framework import status

from movies_api.movies.third_party_api import ThirdPartyApi, ThirdPartyApiWrapper


class ThirdPartyApiTestCase(TestCase):
    """Test ThirdPartyApi and ThirdPartyApiWrapper"""
    def test_json_response(self):
        tpa = ThirdPartyApi('')
        tpa.fetch_json()
        self.assertEqual(tpa.status_code, status.HTTP_200_OK)

    def test_serialized_data(self):
        tpa_wrapper = ThirdPartyApiWrapper('http://127.0.0.1:8000/')
        serialized_data = tpa_wrapper.get_serialized_data()
        next_page_link = serialized_data['next']
        self.assertEqual(next_page_link, 'http://127.0.0.1:8000/?page=2')