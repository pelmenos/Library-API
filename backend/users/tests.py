from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserApiTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "admin@test.com",
            "password": "password123",
            "first_name": "Admin",
            "last_name": "User"
        }
        self.user = User.objects.create_superuser(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_1_login_user(self):
        """1. POST /api/users/token"""
        response = self.client.post(reverse('token_obtain_pair'), {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_5_create_user(self):
        """5. POST /api/users"""
        url = reverse('user-list')
        data = {
            "email": "new@test.com",
            "password": "newpassword123",
            "first_name": "Ivan",
            "last_name": "Ivanov"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_6_get_users(self):
        """6. GET /api/users"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_7_update_user(self):
        """7. PUT /api/users/{id}"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail', args=[self.user.id])
        data = {"first_name": "Updated", "last_name": "Name"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated", response.data)