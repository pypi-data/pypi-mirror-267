from dataclasses import dataclass
from typing import Callable

from jsonschema import ValidationError
from jsonschema.validators import Draft202012Validator

from models.schemas import get_schema


@dataclass
class ValidationIssue:
    location: str
    reason: str


def error_to_issue(error: ValidationError) -> ValidationIssue:
    return ValidationIssue(
        location=f"${'.' if len(error.path) > 0 else ''}{'.'.join(error.path)}",
        reason=error.message,
    )


def validate(schema_code: str) -> Callable[[dict], list[ValidationIssue]]:
    validator = Draft202012Validator(get_schema(schema_code))

    def validate_instance(subject: dict) -> list[ValidationIssue]:
        return list(map(error_to_issue, validator.iter_errors(subject)))

    return validate_instance
