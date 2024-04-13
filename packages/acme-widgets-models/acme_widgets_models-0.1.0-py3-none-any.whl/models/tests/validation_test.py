from typing import Callable

import pytest

from models import validation as sut


@pytest.fixture
def validator_acme_payload_widget_v1() -> Callable[[dict], list[sut.ValidationIssue]]:
    return sut.validate("acme_payload_widget_v1")


def test_should_accept_valid_acme_payload_widget_v1(
    validator_acme_payload_widget_v1, valid_acme_payload_widget_v1
):
    assert validator_acme_payload_widget_v1(valid_acme_payload_widget_v1) == []


def test_should_reject_invalid_acme_payload_widget_v1(
    validator_acme_payload_widget_v1, valid_acme_payload_widget_v1
):
    invalid_acme_payload_widget_v1 = {
        k: v for k, v in valid_acme_payload_widget_v1.items() if k != "batchNo"
    }

    assert validator_acme_payload_widget_v1(invalid_acme_payload_widget_v1) == [
        sut.ValidationIssue("$", "'batchNo' is a required property")
    ]
