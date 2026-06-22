from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        user = get_user_model().objects.create_user(
            email="person@OFTALMI.COM",
            password="test-pass",
            first_name="Test",
            last_name="User",
        )

        self.assertEqual(user.email, "person@oftalmi.com")
        self.assertEqual(user.USERNAME_FIELD, "email")
        self.assertTrue(user.check_password("test-pass"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="test-pass")

    def test_create_superuser_sets_required_flags(self):
        user = get_user_model().objects.create_superuser(
            email="admin@oftalmi.com",
            password="test-pass",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_rejects_invalid_flags(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email="admin@oftalmi.com",
                password="test-pass",
                is_staff=False,
            )
