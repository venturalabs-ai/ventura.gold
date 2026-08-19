"""Exporter tests"""
from core.exporter import export_package


def test_export_json(tmp_path):
    out = export_package([], [], ["generic"], tmp_path)
    pkg = out["package"]
    assert pkg["format"] == "ventura-agent-package/v1"
    assert not str(pkg["format"]).startswith("/")
