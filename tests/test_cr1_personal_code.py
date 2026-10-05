"""CR-1: personas koda pārbaude (tracker/CR-1.md). Viena kritēriju rinda = viens tests.

Sagaidāmās vērtības ņemtas no pieteikuma kritērijiem un līguma docs/openapi.yaml.
OMD pārbaudi (CR-2) aizstāj viltotais klients no conftest.py (fiktūra `client`).
"""


def _submit(client, payload, personal_code):
    payload["personalCode"] = personal_code
    return client.post("/submissions", json=payload)


def _stored_code(client, response):
    # SubmissionCreated līgumā nesatur personalCode; saglabāto vērtību
    # atgriež GET /submissions/{id} (shēma Submission).
    submission_id = response.json()["id"]
    stored = client.get(f"/submissions/{submission_id}")
    assert stored.status_code == 200
    return stored.json()["personalCode"]


def _assert_issue(client, response, issue):
    # Līgums: 400 ValidationError, shēma Error (error.code, error.message,
    # error.details[].field + issue). Iesniegums netiek saglabāts.
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert isinstance(error["message"], str)
    assert {"field": "personalCode", "issue": issue} in error["details"]
    assert client.get("/submissions").json() == []


def test_cr1_ac1_new_format_accepted(client, valid_payload):
    response = _submit(client, valid_payload, "32000000001")
    assert response.status_code == 201
    assert _stored_code(client, response) == "32000000001"


def test_cr1_ac2_hyphen_normalised(client, valid_payload):
    response = _submit(client, valid_payload, "320000-00001")
    assert response.status_code == 201
    assert _stored_code(client, response) == "32000000001"


def test_cr1_ac3_outer_spaces_removed(client, valid_payload):
    response = _submit(client, valid_payload, " 32000000001 ")
    assert response.status_code == 201
    assert _stored_code(client, response) == "32000000001"


def test_cr1_ac4_10_digits_invalid_format(client, valid_payload):
    _assert_issue(
        client, _submit(client, valid_payload, "3200000000"), "INVALID_FORMAT"
    )


def test_cr1_ac5_12_digits_invalid_format(client, valid_payload):
    _assert_issue(
        client, _submit(client, valid_payload, "320000000012"), "INVALID_FORMAT"
    )


def test_cr1_ac6_letter_o_invalid_format(client, valid_payload):
    _assert_issue(
        client, _submit(client, valid_payload, "32000000O01"), "INVALID_FORMAT"
    )


def test_cr1_ac7_missing_field_required(client, valid_payload):
    del valid_payload["personalCode"]
    _assert_issue(client, client.post("/submissions", json=valid_payload), "REQUIRED")


def test_cr1_ac8_old_format_accepted(client, valid_payload):
    response = _submit(client, valid_payload, "311299-21233")
    assert response.status_code == 201
    assert _stored_code(client, response) == "31129921233"


def test_cr1_ac9_hyphen_wrong_place_invalid_format(client, valid_payload):
    _assert_issue(
        client, _submit(client, valid_payload, "3200-0000001"), "INVALID_FORMAT"
    )


# Precizējumi (clarifications), nevis kritēriju tabulas rindas.


def test_cr1_clarification_blank_value_required(client, valid_payload):
    _assert_issue(client, _submit(client, valid_payload, "   "), "REQUIRED")


def test_cr1_clarification_error_does_not_echo_input(client, valid_payload):
    response = _submit(client, valid_payload, "320000000012")
    assert "320000000012" not in response.text
