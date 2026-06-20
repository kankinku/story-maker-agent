#!/usr/bin/env python3
"""Audit portable Hyperagent/Codex skill package fields."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover
    raise SystemExit("jsonschema is required: pip install jsonschema") from exc

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def add_issue(issues: list[dict[str, str]], severity: str, code: str, path: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "path": path, "message": message})


def parse_nested_json(value: Any, path: str, issues: list[dict[str, str]]) -> Any:
    if value is None:
        return None
    if not isinstance(value, str):
        add_issue(issues, "error", "NESTED_JSON_TYPE", path, "Expected nested JSON string.")
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        add_issue(issues, "error", "NESTED_JSON_PARSE", path, str(exc))
        return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_fixture(schema_path: Path, fixture_path: Path, should_pass: bool, issues: list[dict[str, str]]) -> None:
    schema = load_json(schema_path)
    fixture = load_json(fixture_path)
    validator = jsonschema.Draft202012Validator(schema)
    errors = list(validator.iter_errors(fixture))
    if should_pass and errors:
        add_issue(issues, "error", "SCHEMA_FIXTURE_FAIL", str(fixture_path.relative_to(ROOT)), errors[0].message)
    if not should_pass and not errors:
        add_issue(issues, "error", "SCHEMA_INVALID_FIXTURE_PASSED", str(fixture_path.relative_to(ROOT)), "Invalid fixture unexpectedly passed.")


def audit_hyperagent_package() -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    required_files = [
        "metadata.json",
        "manifest.json",
        "SKILL.md",
        "schemas/input.schema.json",
        "schemas/output.schema.json",
        "schemas/lexicon.schema.json",
        "tests/fixtures/valid_input.json",
        "tests/fixtures/invalid_input.json",
        "tests/fixtures/valid_output.json",
        "tests/fixtures/invalid_output.json",
        "tests/fixtures/valid_lexicon.json",
        "tests/fixtures/invalid_lexicon.json",
        "dist/webnovel-production-loop.skill.json",
    ]
    for rel in required_files:
        if not (ROOT / rel).exists():
            add_issue(issues, "error", "MISSING_FILE", rel, "Required package file is missing.")

    if issues:
        return issues

    metadata = load_json(ROOT / "metadata.json")
    manifest = load_json(ROOT / "manifest.json")
    export = load_json(ROOT / "dist" / "webnovel-production-loop.skill.json")

    for key in ["name", "description", "tags", "whenToUse", "authType", "references", "scriptDescriptions", "packageVersion", "bundleDocuments"]:
        if key not in metadata:
            add_issue(issues, "error", "METADATA_KEY_MISSING", f"metadata.json.{key}", "Required metadata key is missing.")

    for key in ["schemaVersion", "id", "name", "version", "routing", "inputs", "outputs", "permissions", "scripts", "validation"]:
        if key not in manifest:
            add_issue(issues, "error", "MANIFEST_KEY_MISSING", f"manifest.json.{key}", "Required manifest key is missing.")

    if metadata.get("packageVersion") != manifest.get("version"):
        add_issue(issues, "error", "VERSION_DRIFT", "metadata.json/packageVersion", "metadata packageVersion and manifest version differ.")

    validate_fixture(ROOT / "schemas" / "input.schema.json", ROOT / "tests" / "fixtures" / "valid_input.json", True, issues)
    validate_fixture(ROOT / "schemas" / "input.schema.json", ROOT / "tests" / "fixtures" / "invalid_input.json", False, issues)
    validate_fixture(ROOT / "schemas" / "output.schema.json", ROOT / "tests" / "fixtures" / "valid_output.json", True, issues)
    validate_fixture(ROOT / "schemas" / "output.schema.json", ROOT / "tests" / "fixtures" / "invalid_output.json", False, issues)
    validate_fixture(ROOT / "schemas" / "lexicon.schema.json", ROOT / "tests" / "fixtures" / "valid_lexicon.json", True, issues)
    validate_fixture(ROOT / "schemas" / "lexicon.schema.json", ROOT / "tests" / "fixtures" / "invalid_lexicon.json", False, issues)

    for rel in metadata.get("bundleDocuments", []):
        if not (ROOT / rel).exists():
            add_issue(issues, "error", "BUNDLE_MISSING", rel, "Bundled document does not exist.")

    for asset in manifest.get("assets", []):
        if isinstance(asset, str):
            add_issue(issues, "error", "ASSET_CHECKSUM_MISSING", asset, "Asset must include path and sha256.")
            continue
        rel = asset.get("path", "")
        path = ROOT / rel
        if not path.exists():
            add_issue(issues, "error", "ASSET_MISSING", rel, "Manifest asset does not exist.")
            continue
        if asset.get("sha256") != sha256(path):
            add_issue(issues, "error", "ASSET_CHECKSUM_DRIFT", rel, "Manifest asset sha256 is missing or stale.")

    for script in manifest.get("scripts", []):
        rel = script.get("path", "")
        path = ROOT / rel
        if not path.exists():
            add_issue(issues, "error", "MANIFEST_SCRIPT_MISSING", rel, "Manifest script does not exist.")
            continue
        for key in ["runtime", "network", "description", "sha256"]:
            if key not in script:
                add_issue(issues, "error", "MANIFEST_SCRIPT_KEY_MISSING", f"{rel}.{key}", "Manifest script key is missing.")
        if script.get("sha256") != sha256(path):
            add_issue(issues, "error", "SCRIPT_CHECKSUM_DRIFT", rel, "Manifest script sha256 is missing or stale.")
        if "timeout_ms" not in script:
            add_issue(issues, "warning", "SCRIPT_TIMEOUT_MISSING", rel, "Script has no timeout_ms budget.")

    for ref in metadata.get("references", []):
        path = ref.get("path")
        url = ref.get("url")
        if path and not (ROOT / path).exists() and not ref.get("optional"):
            add_issue(issues, "warning", "REFERENCE_PATH_MISSING", path, "Reference path is not bundled in this package.")
        if not path and not url:
            add_issue(issues, "warning", "REFERENCE_TARGET_MISSING", ref.get("title", "?"), "Reference has neither path nor url.")

    described_scripts = metadata.get("scriptDescriptions", {})
    actual_scripts = sorted(path.name for path in (ROOT / "scripts").glob("*.py"))
    for script in actual_scripts:
        if script not in described_scripts:
            add_issue(issues, "warning", "SCRIPT_DESCRIPTION_MISSING", f"scripts/{script}", "Script lacks metadata description.")

    if export.get("type") != "skill" or export.get("version") != 1:
        add_issue(issues, "error", "EXPORT_SHAPE", "dist/webnovel-production-loop.skill.json", "Export must be version 1 skill.")
    data = export.get("data", {})
    for key in ["name", "description", "documentation", "tags", "whenToUse", "authType", "credentialSchema", "skillMdBody", "scripts", "references"]:
        if key not in data:
            add_issue(issues, "error", "EXPORT_DATA_KEY_MISSING", f"data.{key}", "Export data key is missing.")

    tags = parse_nested_json(data.get("tags"), "data.tags", issues)
    if tags is not None and not isinstance(tags, list):
        add_issue(issues, "error", "TAGS_NOT_LIST", "data.tags", "Parsed tags must be a list.")

    scripts = parse_nested_json(data.get("scripts"), "data.scripts", issues)
    if scripts is not None:
        if not isinstance(scripts, list):
            add_issue(issues, "error", "SCRIPTS_NOT_LIST", "data.scripts", "Parsed scripts must be a list.")
        else:
            for item in scripts:
                if not all(k in item for k in ["filename", "content", "description"]):
                    add_issue(issues, "error", "SCRIPT_EXPORT_INCOMPLETE", str(item.get("filename")), "Exported script lacks filename, content, or description.")

    documentation = data.get("documentation", "")
    skill_body = data.get("skillMdBody", "")
    if documentation != skill_body:
        add_issue(issues, "warning", "DOC_SKILL_BODY_DRIFT", "data.documentation", "documentation and skillMdBody differ.")
    for rel in metadata.get("bundleDocuments", []):
        if rel not in documentation:
            add_issue(issues, "error", "BUNDLE_NOT_IN_EXPORT", rel, "Bundled document was not included in export documentation.")

    return issues


def audit_codex_project(project_root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    codex_skills = project_root / ".codex" / "skills"
    if not codex_skills.exists():
        add_issue(issues, "warning", "CODEX_SKILLS_MISSING", ".codex/skills", "Project has no local Codex skills directory.")
        return issues

    for skill_dir in sorted(path for path in codex_skills.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        manifest = skill_dir / "manifest.json"
        if not skill_md.exists():
            add_issue(issues, "error", "CODEX_SKILL_BODY_MISSING", str(skill_md), "Codex skill has no SKILL.md.")
        if not manifest.exists():
            add_issue(issues, "warning", "CODEX_SKILL_MANIFEST_MISSING", str(manifest), "Codex skill lacks manifest.json.")
            continue
        doc = load_json(manifest)
        for key in ["schemaVersion", "id", "name", "version", "entrypoint", "routing", "permissions"]:
            if key not in doc:
                add_issue(issues, "error", "CODEX_MANIFEST_KEY_MISSING", f"{manifest}.{key}", "Codex skill manifest key is missing.")
        routing = doc.get("routing", {})
        if not routing.get("whenToUse") or not routing.get("exampleTriggers"):
            add_issue(issues, "error", "CODEX_ROUTING_INCOMPLETE", str(manifest), "Codex skill routing needs whenToUse and exampleTriggers.")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=ROOT.parent, help="Project root containing .codex")
    args = parser.parse_args()

    issues = audit_hyperagent_package() + audit_codex_project(args.project_root.resolve())
    errors = [issue for issue in issues if issue["severity"] == "error"]
    warnings = [issue for issue in issues if issue["severity"] == "warning"]
    result = {
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "error_count": len(errors),
            "warning_count": len(warnings),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
