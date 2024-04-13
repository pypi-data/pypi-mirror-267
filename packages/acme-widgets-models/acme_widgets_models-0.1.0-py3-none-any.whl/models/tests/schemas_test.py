from jsonschema.protocols import Validator
from pytest import mark, raises

from models.schemas import get_schema, get_schemas


@mark.parametrize("_schema_code,schema", get_schemas())
def test_schemas_should_be_valid(_schema_code, schema):
    Validator.check_schema(schema)


@mark.parametrize("schema_code, expected_schema", get_schemas())
def test_get_schema_should_return_specified_schema(schema_code, expected_schema):
    assert get_schema(schema_code) == expected_schema


def test_get_schema_should_raise_useful_error_when_given_invalid_schema_code():
    invalid_schema_code = "some_non_extant_schema_code"
    with raises(
        ValueError,
        match=f"unable to locate '{invalid_schema_code}' at '.+'. is this a valid schema code?",
    ):
        get_schema(invalid_schema_code)
