"""
Load test for the ingestion endpoint — simulates high-volume tenant event traffic.
Run: locust -f infra/load-testing/locustfile.py --host=http://localhost:8000
"""
from locust import HttpUser, task, between


class IngestionUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def post_event(self):
        self.client.post(
            "/v1/events",
            json={
                "event_type": "feature_used",
                "event_payload": {"feature": "dashboard_view"},
            },
            headers={"Authorization": "Bearer <test-jwt>"},
        )
