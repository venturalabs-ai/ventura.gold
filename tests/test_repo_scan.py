from pathlib import Path
from ventura_gold.skills.repository_analyst import RepositoryAnalystSkill


def test_scan_runs():
    skill = RepositoryAnalystSkill(Path.cwd())
    report = skill.generate_report()
    assert "Relatório" in report
    assert "Estatísticas" in report
