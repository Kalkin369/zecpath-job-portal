from rest_framework.test import APITestCase

from core.models.user import User
from core.models.job import Job


class ApplicationTests(APITestCase):

    def setUp(self):

        # Employer
        self.employer_user = User.objects.create_user(
            email="employer@test.com",
            password="test1234",
            role="employer"
        )

        self.employer = self.employer_user.employer

        # Candidate
        self.candidate_user = User.objects.create_user(
            email="candidate@test.com",
            password="test1234",
            role="candidate"
        )

        self.candidate = self.candidate_user.candidate

        # Job
        self.job = Job.objects.create(
            employer=self.employer,
            title="Python Developer",
            description="Backend Role",
            skills="python,django",
            experience=2,
            location="Kerala",
            job_type="full_time"
        )

    def test_candidate_can_view_own_applications(self):

        self.client.force_authenticate(
            user=self.candidate_user
        )

        response = self.client.get(
            "/api/applications/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_employer_can_view_job_applicants(self):

        self.client.force_authenticate(
            user=self.employer_user
        )

        response = self.client.get(
            f"/api/applications/job/{self.job.id}/applicants/"
        )

        self.assertEqual(
            response.status_code,
            200
        )