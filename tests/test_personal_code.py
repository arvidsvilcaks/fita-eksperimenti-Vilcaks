"""CR-1: personas koda formāta pārbaude. Personas kodi ir sintētiski."""

import logging

import pytest

from app import storage


def _issues(response):
    return response.json()["error"]["details"]


@pytest.mark.parametrize(
    ("code", "stored"),
    [
        ("32000000001", "32000000001"),  # 1
        ("320000-00001", "32000000001"),  # 2
        (" 32000000001 ", "32000000001"),  # 3
        ("311299-21233", "31129921233"),  # 8
    ],
)
def test_valid_personal_code_is_stored_normalized(client, valid_payload, code, stored):
    valid_payload["personalCode"] = code
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 201
    saved = client.get(f"/submissions/{response.json()['id']}").json()
    assert saved["personalCode"] == stored


@pytest.mark.parametrize(
    "code",
    [
        "3200000000",  # 4: 10 cipari
        "320000000012",  # 5: 12 cipari
        "32000000O01",  # 6: burts O
        "3200-0000001",  # 9: defise nepareizā vietā
        "٣٢٠٠٠٠٠٠٠٠١",  # Unicode cipari nav derīgi
        "32000 000001",  # atstarpe vidū
    ],
)
def test_invalid_personal_code_returns_400(client, valid_payload, fake_omd, code):
    valid_payload["personalCode"] = code
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    assert _issues(response) == [{"field": "personalCode", "issue": "INVALID_FORMAT"}]
    assert code not in response.text
    assert storage.get("IES-2026-000001") is None
    assert fake_omd.calls == []


@pytest.mark.parametrize("code", [None, 32000000001])
def test_non_string_personal_code_returns_invalid_format(
    client, valid_payload, fake_omd, code
):
    valid_payload["personalCode"] = code
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    assert _issues(response) == [{"field": "personalCode", "issue": "INVALID_FORMAT"}]
    assert "32000000001" not in response.text
    assert storage.get("IES-2026-000001") is None
    assert fake_omd.calls == []


def test_missing_personal_code_returns_required(client, valid_payload, fake_omd):  # 7
    del valid_payload["personalCode"]
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 400
    assert _issues(response) == [{"field": "personalCode", "issue": "REQUIRED"}]
    assert storage.get("IES-2026-000001") is None
    assert fake_omd.calls == []


@pytest.mark.parametrize("code", ["", "   "])
def test_blank_personal_code_returns_required(client, valid_payload, fake_omd, code):
    valid_payload["personalCode"] = code
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 400
    assert _issues(response) == [{"field": "personalCode", "issue": "REQUIRED"}]
    assert storage.get("IES-2026-000001") is None
    assert fake_omd.calls == []


def test_personal_code_is_not_logged(client, valid_payload, caplog):
    caplog.set_level(logging.DEBUG)
    valid_payload["personalCode"] = "320000-00001"
    assert client.post("/submissions", json=valid_payload).status_code == 201
    valid_payload["personalCode"] = "32000000O01"
    assert client.post("/submissions", json=valid_payload).status_code == 400
    for code in ("32000000001", "320000-00001", "32000000O01"):
        assert code not in caplog.text
