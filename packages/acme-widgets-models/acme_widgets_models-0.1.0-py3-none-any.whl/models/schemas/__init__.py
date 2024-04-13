import json
from glob import glob
from os.path import basename, dirname, isfile, join


def get_schemas() -> list[tuple[str, dict]]:
    result = []
    schema_glob = join(dirname(dirname(__file__)), "schemas", "*.json")
    for schema_path in glob(schema_glob):
        schema_code = basename(schema_path).rstrip(".json")
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            result.append((schema_code, json.load(schema_file)))

    return result


def get_schema(schema_code: str) -> dict:
    schema_path = join(
        dirname(dirname(__file__)), "schemas", f"{schema_code.strip()}.json"
    )
    if not isfile(schema_path):
        raise ValueError(
            f"unable to locate '{schema_code}' at '{schema_path}'. is this a valid schema code?"
        )

    with open(schema_path, mode="r", encoding="utf-8") as schema_file:
        return json.load(schema_file)
