"""Test dell'API con il client di test di Flask (senza browser)."""


def test_api_requires_login(client):
    response = client.get("/api/apps")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_api_returns_applications_as_json(client):
    client.post("/auth/login", data={"username": "admin", "password": "admin123"})
    response = client.get("/api/apps")
    assert response.status_code == 200
    names = [a["name"] for a in response.get_json()]
    assert names == ["7-Zip", "VLC"]
