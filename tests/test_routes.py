def test_index_route(client):
    response = client.get("/auth/")
    assert response.status_code == 200
    assert b"hello" in response.data
