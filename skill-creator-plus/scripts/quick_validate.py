#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64
SCRIPT_SUFFIXES = {".py", ".sh", ".ps1", ".js", ".ts"}


def has_business_scripts(skill_path):
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.exists() or not scripts_dir.is_dir():
        return False
    for path in scripts_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCRIPT_SUFFIXES:
            continue
        # Ignore obvious QA/test runners when deciding if business scripts exist.
        lower_name = path.name.lower()
        if "qa" in lower_name or lower_name.startswith("test_") or lower_name.endswith("_test.py"):
            continue
        return True
    return False


def has_qa_script(skill_path):
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.exists() or not scripts_dir.is_dir():
        return False
    for path in scripts_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCRIPT_SUFFIXES:
            continue
        lower_name = path.name.lower()
        if (
            "qa" in lower_name
            or "validate" in lower_name
            or lower_name.startswith("test_")
            or lower_name.endswith("_test.py")
        ):
            return True
    return False


def has_qa_section(content):
    return re.search(r"^##+\s+.*(?:qa|test)", content, re.IGNORECASE | re.MULTILINE) is not None


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    allowed_properties = {"name", "description", "license", "allowed-tools", "metadata"}

    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        allowed = ", ".join(sorted(allowed_properties))
        unexpected = ", ".join(sorted(unexpected_keys))
        return (
            False,
            f"Unexpected key(s) in SKILL.md frontmatter: {unexpected}. Allowed properties are: {allowed}",
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)",
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
            )
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return (
                False,
                f"Name is too long ({len(name)} characters). "
                f"Maximum is {MAX_SKILL_NAME_LENGTH} characters.",
            )

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return (
                False,
                f"Description is too long ({len(description)} characters). Maximum is 1024 characters.",
            )

    if has_business_scripts(skill_path):
        if not has_qa_section(content):
            return False, "Script-based skill must include a QA/Test section in SKILL.md body"
        qa_checklist = skill_path / "references" / "qa-checklist.md"
        if not qa_checklist.exists():
            return False, "Script-based skill must include references/qa-checklist.md"
        if not has_qa_script(skill_path):
            return False, "Script-based skill must include at least one QA/test script under scripts/"

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
