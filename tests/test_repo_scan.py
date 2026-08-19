from pathlib import Path
from ventura_gold.skills.repository.analyst import RepositoryAnalystSkill
from ventura_gold.skills.review.auditor import ReviewAuditorSkill
from ventura_gold.skills.docs.generator import DocsGeneratorSkill


def test_scan_generates_report():
    skill = RepositoryAnalystSkill(Path.cwd())
    report = skill.generate_report()
    assert "reposit" in report.lower()


def test_review_report():
    report = ReviewAuditorSkill(Path.cwd()).report()
    assert "auditoria" in report.lower() or "revisao" in report.lower() or "Revisao" in report


def test_docs_outline():
    outline = DocsGeneratorSkill(repo_path=Path.cwd()).generate_readme_outline()
    assert "document" in outline.lower()
