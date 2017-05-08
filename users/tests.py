from django.test import TestCase

from users.models import Account
from bmlist_service import UserAccountService

# Create your tests here.

class UserTestCases(TestCase):
    def setUp(self):
        # Account.objects.create(email='abc@126.com',passwd='12345')
        self.user_account_service = UserAccountService()

    def test_signup_and_signin(self):
        account = Account()
        account.email='test01@tt.com'
        account.passwd='nopwd'
        account_id = self.user_account_service.signup(account)

        email = 'test01@tt.com'
        passwd = 'nopwd'
        account  = self.user_account_service.signin(passwd,email)
        print (account)
        self.assertEqual(account_id,account.id)

