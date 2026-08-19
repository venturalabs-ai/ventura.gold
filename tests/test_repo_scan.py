from pathlib import Path
from ventura_gold.skills.repository_analyst import RepositoryAnalystSkill


def test_scan_generates_report():
    skill = RepositoryAnalystSkill(Path.cwd())
    report = skill.generate_report()
    assert "reposit" in report.lower()
