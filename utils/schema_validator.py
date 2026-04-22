from jsonschema import validate


def validate_schema(data, schema):
    validate(instance=data, schema=schema)
    