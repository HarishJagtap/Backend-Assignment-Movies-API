from django.test import TestCase

from movies_api.register.token_manager import TokenManager


class TokenManagerTestCase(TestCase):
    def test_token_manager(self):
        tm = TokenManager('test_user', 'test_pwd')
        self.assertTrue(tm._user_verified)
        self.assertIsNotNone(tm.get_access_token())
