from ventura_gold.core.validator import validate_project


def test_validate():
    r = validate_project()
    assert "valid" in r
