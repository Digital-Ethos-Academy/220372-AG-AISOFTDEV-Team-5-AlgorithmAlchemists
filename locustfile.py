"""Locust performance harness for core endpoints."""
from __future__ import annotations

from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def overview(self):
        self.client.get("/overview")

    @task
    def org(self):
        self.client.get("/org")

    @task
    def roles(self):
        self.client.get("/roles", params={"query": "Team"})

    @task
    def qa(self):
        self.client.post("/qa", params={"question": "Who owns API?"})

    @task
    def recommendation(self):
        self.client.post("/recommendation", params={"user_id": "demo"})

    @task
    def quiz(self):
        self.client.get("/quiz")

    @task
    def metrics(self):
        self.client.get("/metrics")
