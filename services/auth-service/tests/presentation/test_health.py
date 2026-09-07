from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):

    def test_health_check_returns_ok(self):
        response = self.client.get("/api/v1/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "auth-service",
            },
        )

    def test_health_check_rejects_post(self):
        response = self.client.post("/api/v1/health/")

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )