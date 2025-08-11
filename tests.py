from django.test import TestCase
from ninja.testing import TestClient
from .api import api
from .models import User

class BlogTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Получаем JWT токен через эндпоинт авторизации
        response = self.client.post("/auth/jwt/", json={"username": "testuser", "password": "testpass"})
        self.token = response.json().get("access")

    def test_article_creation(self):
        response = self.client.post(
            "/articles/",
            json={"title": "Тест", "content": "Тестовое содержание"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Тест")

    def test_unauthorized_access(self):
        response = self.client.post(
            "/articles/",
            json={"title": "Тест", "content": "Тестовое содержание"}
        )
        self.assertEqual(response.status_code, 401)

    def test_comment_flow(self):
        article_res = self.client.post(
            "/articles/",
            json={"title": "Тестовая статья", "content": "Содержание"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        article_id = article_res.json()["id"]

        comment_res = self.client.post(
            f"/articles/{article_id}/comments",
            json={"text": "Отличная статья!"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(comment_res.status_code, 200)

        comments_res = self.client.get(f"/articles/{article_id}/comments")
        self.assertEqual(len(comments_res.json()), 1)