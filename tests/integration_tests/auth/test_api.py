import pytest
from httpx import AsyncClient

from tests.conftest import get_db_null_pool


@pytest.fixture(scope="module")
async def delete_all_users():
    async for _db in get_db_null_pool():
        await _db.users.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "email, password",
    [
        ("kot@pes.com", "1234"),
        ("kot@kot.com", "1234"),
        ("pes@pes.com", "1234"),
    ],
)
async def test_authorization_flow(
    email,
    password,
    delete_all_users,
    ac: AsyncClient,
):
    resp_reg = await ac.post("/auth/register", json={"email": email, "password": password})
    assert resp_reg.status_code == 200

    resp_login = await ac.post("/auth/login", json={"email": email, "password": password})
    assert resp_login.status_code == 200

    resp_me = await ac.get("/auth/me")
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert isinstance(user, dict)
    assert user["email"] == email
    assert "id" in user
    assert "password" not in user
    assert "hashed_password" not in user

    resp_logout = await ac.post("auth/logout")
    assert resp_logout.status_code == 200

    after_logout_response = await ac.get("/auth/me")
    assert after_logout_response.status_code == 401
