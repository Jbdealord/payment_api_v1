from django.db import models
from django.test import TestCase

from payment_api_v1.models import Account


class AccountModelStructureTestCase(TestCase):

    def test_account_has_email(self):
        email = Account._meta.get_field('email')
        self.assertIsInstance(email, models.EmailField)

    def test_email_field_arguments(self):
        email = Account._meta.get_field('email')

        self.assertFalse(email.null)
        self.assertFalse(email.blank)
