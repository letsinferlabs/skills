#!/usr/bin/env python3
"""Validate the portable public Let’s Infer skill package."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EXPECTED_SKILLS = {
    "letsinfer-benchmark",
    "letsinfer-cli",
    "letsinfer-engine-authoring",
    "letsinfer-runtime-authoring",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTTPS_RE = re.compile(r"https://[^\s)>]+")
FORBIDDEN_PUBLIC_TEXT = (
    "/shipit",
    "bypass-verifiers",
    "verifier_bypass",
    "runtime-review",
    "maintainer bypass",
    "maintainer override",
    "letsinferlabs/work",
    "scratchpad/",
)
ALLOWED_SKILL_CHILDREN = {"SKILL.md", "agents", "references", "scripts"}


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def parse_frontmatter(path: pathlib.Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            fail(f"{path.relative_to(ROOT)}: frontmatter must use flat key/value fields")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in values or not value:
            fail(f"{path.relative_to(ROOT)}: invalid or duplicate field {key!r}")
        values[key] = value.strip('"\'')
    if set(values) != {"name", "description"}:
        fail(
            f"{path.relative_to(ROOT)}: portable frontmatter must contain only "
            "name and description"
        )
    return values, text


def validate_public_text(path: pathlib.Path, text: str) -> None:
    lowered = text.lower()
    for value in FORBIDDEN_PUBLIC_TEXT:
        if value.lower() in lowered:
            fail(f"{path.relative_to(ROOT)}: forbidden public release/private text: {value}")
    if "../../" in text:
        fail(f"{path.relative_to(ROOT)}: skill package cannot escape through ../../ links")


def validate_links(path: pathlib.Path, text: str) -> set[str]:
    urls: set[str] = set()
    for target in MARKDOWN_LINK_RE.findall(text):
        if target.startswith("https://"):
            urls.add(target)
            continue
        if "://" in target:
            fail(f"{path.relative_to(ROOT)}: non-HTTPS link is forbidden: {target}")
        resolved = (path.parent / target.split("#", 1)[0]).resolve()
        if not resolved.is_relative_to(ROOT.resolve()) or not resolved.exists():
            fail(f"{path.relative_to(ROOT)}: broken or escaping relative link: {target}")
    for url in HTTPS_RE.findall(text):
        urls.add(url.rstrip(".,;"))
    for url in urls:
        if url.startswith("https://github.com/letsinferlabs/"):
            match = re.match(
                r"https://github\.com/letsinferlabs/([^/]+)(?:/(.*))?$", url
            )
            assert match is not None
            repository, suffix = match.groups()
            if repository not in {"letsinfer", "runtimes", "skills"}:
                fail(f"{path.relative_to(ROOT)}: unapproved Let’s Infer repository: {url}")
            if suffix and suffix.startswith("blob/") and not suffix.startswith("blob/main/"):
                fail(f"{path.relative_to(ROOT)}: living contract link must use main: {url}")
    return urls


def validate_openai_metadata(skill: str, path: pathlib.Path) -> None:
    text = path.read_text(encoding="utf-8")
    required = ("display_name:", "short_description:", "default_prompt:")
    for field in required:
        if field not in text:
            fail(f"{path.relative_to(ROOT)}: missing {field[:-1]}")
    if f"${skill}" not in text:
        fail(f"{path.relative_to(ROOT)}: default_prompt must mention ${skill}")
    validate_public_text(path, text)


def validate_skill(skill_dir: pathlib.Path) -> set[str]:
    skill = skill_dir.name
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        fail(f"skills/{skill}: missing SKILL.md")
    if not NAME_RE.fullmatch(skill) or len(skill) > 64:
        fail(f"skills/{skill}: invalid portable skill name")
    values, text = parse_frontmatter(path)
    if values["name"] != skill:
        fail(f"skills/{skill}: folder and frontmatter name differ")
    description = values["description"]
    if len(description) < 50 or len(description) > 500:
        fail(f"skills/{skill}: description must be 50–500 characters")
    if "Let’s Infer" not in description:
        fail(f"skills/{skill}: description must remain product-scoped")
    validate_public_text(path, text)
    urls = validate_links(path, text)
    if not any(url.startswith("https://github.com/letsinferlabs/") for url in urls):
        fail(f"skills/{skill}: missing canonical public contract link")
    unexpected = {child.name for child in skill_dir.iterdir()} - ALLOWED_SKILL_CHILDREN
    if unexpected:
        fail(f"skills/{skill}: unexpected non-portable content: {sorted(unexpected)}")
    agents = skill_dir / "agents"
    if set(child.name for child in agents.iterdir()) != {"openai.yaml"}:
        fail(f"skills/{skill}: agents must contain exactly openai.yaml")
    validate_openai_metadata(skill, agents / "openai.yaml")
    supporting = {
        str(file.relative_to(skill_dir))
        for folder in ("references", "scripts")
        if (skill_dir / folder).is_dir()
        for file in (skill_dir / folder).rglob("*")
        if file.is_file()
    }
    expected_supporting = (
        {"references/runtime-pack.md", "scripts/pack_runtime.py"}
        if skill == "letsinfer-runtime-authoring"
        else set()
    )
    if supporting != expected_supporting:
        fail(
            f"skills/{skill}: unexpected supporting resources: "
            f"{sorted(supporting ^ expected_supporting)}"
        )
    for relative in sorted(supporting):
        supporting_path = skill_dir / relative
        supporting_text = supporting_path.read_text(encoding="utf-8")
        validate_public_text(supporting_path, supporting_text)
        if supporting_path.suffix == ".md":
            urls.update(validate_links(supporting_path, supporting_text))
        elif supporting_path.suffix == ".py":
            try:
                compile(supporting_text, str(supporting_path), "exec")
            except SyntaxError as error:
                fail(f"{supporting_path.relative_to(ROOT)}: invalid Python: {error}")
    for file in skill_dir.rglob("*"):
        if file.is_file() and file.stat().st_mode & 0o111:
            fail(f"{file.relative_to(ROOT)}: executable skill payloads are not allowed")
    return urls


def validate_index() -> None:
    value = json.loads((ROOT / "skills.sh.json").read_text(encoding="utf-8"))
    groups = value.get("groupings")
    if not isinstance(groups, list):
        fail("skills.sh.json: groupings must be an array")
    listed = [skill for group in groups for skill in group.get("skills", [])]
    if set(listed) != EXPECTED_SKILLS or len(listed) != len(EXPECTED_SKILLS):
        fail("skills.sh.json: every public skill must appear exactly once")


def validate_readme() -> set[str]:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    validate_public_text(path, text)
    for skill in EXPECTED_SKILLS:
        if skill not in text:
            fail(f"README.md: missing {skill}")
    for harness in ("Codex", "Claude Code", "Cursor", "Grok Build", "DeepSeek Harness", "Hermes Agent"):
        if harness not in text:
            fail(f"README.md: missing harness documentation for {harness}")
    if "npx skills add letsinferlabs/skills" not in text:
        fail("README.md: missing portable install command")
    return validate_links(path, text)


def check_urls(urls: set[str]) -> None:
    for url in sorted(urls):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "letsinfer-skills-validator/1"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.status < 200 or response.status >= 400:
                    fail(f"public link returned HTTP {response.status}: {url}")
        except (urllib.error.URLError, TimeoutError) as error:
            fail(f"public link is unavailable: {url}: {error}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-urls", action="store_true")
    arguments = parser.parse_args()
    if not SKILLS_ROOT.is_dir():
        fail("missing skills directory")
    actual = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    if actual != EXPECTED_SKILLS:
        fail(f"expected exactly {sorted(EXPECTED_SKILLS)}, found {sorted(actual)}")
    urls = validate_readme()
    for skill in sorted(EXPECTED_SKILLS):
        urls.update(validate_skill(SKILLS_ROOT / skill))
    validate_index()
    if arguments.check_urls:
        check_urls(urls)
    print(f"PASS {len(EXPECTED_SKILLS)} portable Let’s Infer skills")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, ValidationError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
