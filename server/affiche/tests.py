from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from accounts.models import CustomUser
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            user_type=2,
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.user_type, 2)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            user_type=1,
        )
        self.assertTrue(admin_user.is_admin())
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_is_admin_method(self):
        user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="testpass123",
            user_type=2,
        )
        admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            user_type=1,
        )
        self.assertFalse(user.is_admin())
        self.assertTrue(admin.is_admin())

    def test_unique_email(self):
        # Создаем первого пользователя
        User.objects.create_user(
            username="user1",
            email="test@example.com",
            password="testpass123",
        )
        # Пытаемся создать второго пользователя с таким же email
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="user2",
                email="test@example.com",
                password="testpass123",
            )

    def test_unique_username(self):
        # Создаем первого пользователя
        User.objects.create_user(
            username="testuser",
            email="test1@example.com",
            password="testpass123",
        )
        # Пытаемся создать второго пользователя с таким же username
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="testuser",
                email="test2@example.com",
                password="testpass123",
            )

    def test_create_user_without_username_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="",
                email="user@example.com",
                password="testpass123",
            )

    def test_create_superuser_must_be_staff_and_superuser(self):
        # Попытка создать суперпользователя без is_staff=True
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="badadmin",
                email="badadmin@example.com",
                password="adminpass123",
                is_staff=False,
                is_superuser=True,
                user_type=1,
            )
        # Попытка создать суперпользователя без is_superuser=True
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="badadmin2",
                email="badadmin2@example.com",
                password="adminpass123",
                is_staff=True,
                is_superuser=False,
                user_type=1,
            )

    def test_user_str_method(self):
        user = User.objects.create_user(
            username="struser",
            email="struser@example.com",
            password="testpass123",
            user_type=2,
        )
        self.assertEqual(str(user), "struser")

    def test_user_type_choices_validation(self):
        # user_type принимает только определённые значения
        user = User(
            username="invalidtype",
            email="invalid@example.com",
            user_type=99
        )
        with self.assertRaises(ValidationError):
            user.full_clean()