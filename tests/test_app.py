# tests/test_app.py

import unittest
import os
os.environ["TESTING"] = "true"

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        # Ethan's home route passes title="Ethan Jin" into render_template
        assert "Ethan Jin" in html

    def test_timeline(self):
        # GET should start empty since each test run uses a fresh in-memory db
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # POST a valid timeline post
        post_response = self.client.post("/api/timeline_post", data={
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post"
        })
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "Test User"

        # Confirm a follow-up GET reflects the new post
        get_response = self.client.get("/api/timeline_post")
        get_json = get_response.get_json()
        assert len(get_json["timeline_posts"]) == 1
        assert get_json["timeline_posts"][0]["name"] == "Test User"

        # Confirm the /timeline page itself renders
        page_response = self.client.get("/timeline")
        assert page_response.status_code == 200

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I am John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I am John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

    def test_health(self):
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()

        # Overall verdict
        assert json["status"] == "healthy"

        # Flask itself answered
        assert json["checks"]["flask"]["ok"] is True

        # The database leg actually ran. This is the whole point of the
        # endpoint: page routes render hardcoded lists and never touch
        # the db, so only this route exercises the mysql container.
        mysql = json["checks"]["mysql"]
        assert mysql["ok"] is True
        assert mysql["rows"] == 0
        assert isinstance(mysql["latency_ms"], float)


if __name__ == "__main__":
    unittest.main()
