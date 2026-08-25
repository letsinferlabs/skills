# Let’s Infer skills contributor instructions

This repository is the public, harness-neutral source for Let’s Infer agent
skills. Keep every skill useful in Codex, Claude Code, Cursor, Grok Build,
DeepSeek Harness, Hermes Agent, and other implementations of the `SKILL.md`
convention.

## Product boundary

- Public skills cover operation, runtime authoring, Engine authoring, and
  benchmarking.
- Repository-maintainer release authorization, privileged commands,
  credentials, allowlists, and private operational procedures do not belong in
  this repository.
- Link to canonical files in `letsinferlabs/letsinfer` and
  `letsinferlabs/runtimes`. Never copy private context or link to private
  repositories, workspace paths, or scratchpads.
- Prefer the checked-out public contract when an agent is already inside that
  repository; otherwise use the public GitHub link in the skill.

## Skill format

- Put each skill exactly at `skills/<skill-name>/SKILL.md`.
- The folder and frontmatter `name` must match and use namespaced kebab-case.
- Use only the portable `name` and `description` frontmatter fields.
- Keep descriptions concise and precise enough for automatic selection.
- Do not assume one harness’s tool names, approval UI, subagents, hooks, or
  slash-command implementation.
- Add supporting files only when a workflow cannot be expressed clearly with
  the public product contracts. Do not add executable code casually.

## Validation

Run `python3 tools/validate_skills.py`. Preserve the exact four-skill public
surface unless a reviewed product decision changes it. Keep commits focused,
and never add generated evidence, model data, build output, secrets, or local
machine state.
