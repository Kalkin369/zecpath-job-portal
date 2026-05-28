from rest_framework.test import APITestCase

from core.models.user import User


class JobTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="employer@test.com",
            password="test1234",
            role="employer"
        )

    def test_employer_create_job(self):

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            "title": "Python Developer",
            "description": "Backend Developer Role",
            "skills": "python,django,rest api",
            "experience": 2,
            "location": "Kerala",
            "job_type": "full_time"
        }

        response = self.client.post(
            "/api/jobs/",
            data
        )

        self.assertEqual(
            response.status_code,
            201
        )

    def test_candidate_cannot_create_job(self):

        candidate_user = User.objects.create_user(
            email="candidate@test.com",
            password="test1234",
            role="candidate"
        )

        self.client.force_authenticate(
            user=candidate_user
        )

        response = self.client.post(
            "/api/jobs/",
            {}
        )

        self.assertEqual(
            response.status_code,
            403
        )