from pathlib import Path
from ventura_gold.core.validator import validate_all


def test_validate_all():
    errors, warnings = validate_all(Path.cwd())
    assert isinstance(errors, list)
    assert isinstance(warnings, list)
