from pytest import fixture

from models.schemas import get_schema


@fixture
def schema_acme_payload_widget_v1() -> dict:
    return get_schema("acme_payload_widget_v1")


@fixture
def valid_acme_payload_widget_v1() -> dict:
    return {
        "batchNo": "123456",
        "syntheticId": "acme:unit-test:abcdef",
    }
