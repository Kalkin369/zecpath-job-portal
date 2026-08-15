from rest_framework.test import APITestCase

from core.models.user import User


class AuthTests(APITestCase):

    def test_candidate_registration(self):

        data = {
            "email": "candidate@test.com",
            "password": "test1234",
            "role": "candidate",
        }

        response = self.client.post("/api/auth/signup/", data)

        self.assertEqual(response.status_code, 201)

        # Check automatic profile creation
        user = User.objects.get(email="candidate@test.com")

        self.assertTrue(hasattr(user, "candidate"))

    def test_employer_registration(self):

        data = {
            "email": "employer@test.com",
            "password": "test1234",
            "role": "employer",
        }

        response = self.client.post("/api/auth/signup/", data)

        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email="employer@test.com")

        self.assertTrue(hasattr(user, "employer"))

    def test_login(self):

        User.objects.create_user(
            email="login@test.com", password="test1234", role="candidate"
        )

        response = self.client.post(
            "/api/auth/login/", {"email": "login@test.com", "password": "test1234"}
        )

        self.assertEqual(response.status_code, 200)
