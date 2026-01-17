def create_user_and_token(client):
    client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )
    res = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )
    return res.json()["access_token"]

def create_user_and_token(client):
    client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )
    res = client.post(
        "/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )
    return res.json()["access_token"]

def test_list_tasks(client):
    token = create_user_and_token(client)

    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_tasks(client):
    token = create_user_and_token(client)

    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task(client):
    token = create_user_and_token(client)

    res = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Old"},
    )
    task_id = res.json()["id"]

    res = client.patch(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated"},
    )

    assert res.status_code == 200
    assert res.json()["title"] == "Updated"
