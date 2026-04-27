from jsonschema import validate, ValidationError


def validate_schema(data: dict, schema: dict) -> None:
    """
    Validate data against a JSON schema.
    Raises ValueError with the failing field path and reason.

    Example
    -------
    USER_SCHEMA = {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
            "id":   {"type": "integer"},
            "name": {"type": "string"},
        }
    }
    validate_schema(response.json(), USER_SCHEMA)
    """
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        field_path = " → ".join(str(p) for p in e.absolute_path) or "root"
        raise ValueError(
            f"Schema validation failed at '{field_path}': {e.message}"
        ) from e


def validate_response(response, schema: dict) -> None:
    """
    Convenience wrapper for API responses — calls .json() automatically.

    Usage
    -----
    validate_response(client.get("/users/1"), USER_SCHEMA)
    """
    validate_schema(response.json(), schema)
    