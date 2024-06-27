from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class UserListViewTests(TestCase):
    """Класс для теста списка пользователей"""

    def setUp(self):
        for i in range(12):
            User.objects.create(
                email=f"user{i:02}@example.com",
                password="password123",
                first_name="User",
                last_name=f"Last {i}",
                username=f"user{i:02}",
            )

    def test_user_list_view_template(self):
        """Используется правильный шаблон и код ответа"""
        response = self.client.get(reverse("users:user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_list.html")

    def test_user_list_view_context(self):
        """Шаблон сформирован с правильным контекстом"""
        response = self.client.get(reverse("users:user_list"))
        self.assertTrue("users" in response.context)
        self.assertEqual(len(response.context["users"]), 10)

    def test_user_list_pagination(self):
        """Пагинация отрабатывается корректно"""
        response = self.client.get(reverse("users:user_list"))
        self.assertTrue("paginator" in response.context)
        self.assertEqual(
            str(response.context.get("page_obj")), "<Page 1 of 2>"
        )


class UserViewsTests(TestCase):
    """Класс для теста пользователя"""

    def setUp(self):
        for i in range(12):
            User.objects.create(
                email=f"user{i:02}@example.com",
                password="password123",
                first_name="User",
                last_name=f"Last {i}",
                username=f"user{i:02}",
                is_active=True,
            )
        self.user = User.objects.last()
        self.authorized_client = Client()
        self.authorized_client.force_login(user=self.user)

    def test_signup_view_get(self):
        """Используется правильный шаблон и код ответа"""
        response = self.client.get(reverse("users:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/signup.html")

    def test_signup_view_post(self):
        """Новый пользователь создается"""
        response = self.client.post(
            reverse("users:signup"),
            {
                "email": "user99@example.com",
                "password1": "Gfhjkm12345",
                "password2": "Gfhjkm12345",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            User.objects.filter(email="user99@example.com").exists()
        )

    def test_profile_view_get(self):
        """Профиль зарегистрированного пользователя открывается"""
        response = self.authorized_client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_profile_view_post(self):
        """Данные пользователя изменяются корректно"""
        response = self.authorized_client.post(
            reverse("users:profile"),
            {
                "first_name": "NewFirstName",
                "last_name": "NewLastName",
                "username": "newusername",
                "email": "user1@example.com",
                "new_email": "newemail@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            User.objects.filter(email="newemail@example.com").exists()
        )
        user = User.objects.get(email="newemail@example.com")
        self.assertEqual(user.first_name, "NewFirstName")
        self.assertEqual(user.last_name, "NewLastName")
        self.assertEqual(user.username, "newusername")
        self.assertFalse(user.is_active)

    def test_activate_view_valid_token(self):
        """Валидация правильного токена пользователя аткивирует его"""
        self.user.is_active = False
        self.user.save()
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(
            reverse("users:activate", args=[uid, token])
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_view_invalid_token(self):
        """Запрос с неправильным токеном перенаправляет на страницу ошибки"""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = "invalid-token"
        response = self.client.get(
            reverse("users:activate", args=[uid, token])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activation_invalid.html")

    def test_user_detail_view_template(self):
        """Используется правильный шаблон и код ответа"""
        response = self.client.get(
            reverse("users:user_detail", args=[self.user.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_detail.html")

    def test_user_detail_view_context(self):
        """Шаблон сформирован с правильным контекстом"""
        response = self.client.get(
            reverse("users:user_detail", args=[self.user.id])
        )
        self.assertTrue("object" in response.context)
        self.assertEqual(response.context["object"], self.user)
