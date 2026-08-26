# Let’s Infer agent skills

Official, portable skills for operating Let’s Infer and developing model
runtimes. Each skill follows the open `SKILL.md` convention and contains no
agent-specific executable code.

## Skills

| Skill | Use it for |
| --- | --- |
| `letsinfer-cli` | Install, operate, inspect, update, and troubleshoot Let’s Infer. |
| `letsinfer-runtime-authoring` | Create, port, optimize, and qualify a runtime candidate. |
| `letsinfer-engine-authoring` | Change Engine internals or add an Engine Let’s Infer does not yet support. |
| `letsinfer-benchmark` | Run and interpret reproducible runtime benchmarks and PR verification. |

Publication authorization and repository-maintainer procedures are not part of
this public skill set.

## Install

The portable installer detects supported coding agents and lets you choose the
skills and destinations:

```bash
npx skills add letsinferlabs/skills
```

Target one harness explicitly:

```bash
npx skills add letsinferlabs/skills --agent codex
npx skills add letsinferlabs/skills --agent claude-code
npx skills add letsinferlabs/skills --agent cursor
npx skills add letsinferlabs/skills --agent grok
```

For a project using DeepSeek Harness, install to the shared project location:

```bash
npx skills add letsinferlabs/skills --agent universal
```

DeepSeek Harness discovers the resulting `.agents/skills/` directory. For
Hermes Agent, add this repository as a GitHub tap:

```bash
hermes skills tap add letsinferlabs/skills
```

Then browse the tap and install the skills you want. Hermes can also install a
skill directly by its GitHub repository path.

## Use

Agents can select a skill automatically from its description. Explicit
invocation varies by harness:

```text
$letsinfer-cli help me safely upgrade this installed model runtime
/letsinfer-runtime-authoring add a runtime for this model and target
/letsinfer-engine-authoring adapt this new inference Engine
/letsinfer-benchmark verify this runtime pull request
```

The dollar form is common in Codex; slash invocation is common in Claude Code,
Cursor, Grok Build, and Hermes. Ordinary natural-language requests also work
when the harness supports automatic skill selection.

## Compatibility

These skills intentionally use only the shared `name` and `description`
frontmatter fields. They are compatible with harnesses that implement the
Agent Skills directory convention, including:

- Codex: `.agents/skills/`;
- Claude Code: `.claude/skills/`;
- Cursor: `.agents/skills/` or `.cursor/skills/`;
- Grok Build: `.agents/skills/` or `.grok/skills/`;
- DeepSeek Harness: `.agents/skills/` or `.dsh/skills/`; and
- Hermes Agent: GitHub taps, skills.sh, or direct skill URLs.

The optional `agents/openai.yaml` files improve presentation in OpenAI
surfaces. Other harnesses ignore them.

## Updates

Use your installer’s normal update mechanism:

```bash
npx skills check
npx skills update
```

Hermes installations use `hermes skills check` and `hermes skills update`.
The repository’s `main` branch is the current skill source; Git history and
installer locks retain exact prior identities. Separate Git tags are not
required.

## Trust and security

Review skills before installing them: they guide an agent that may have your
filesystem and shell permissions. This repository ships Markdown instructions,
presentation metadata, and one narrow runtime-pack validation helper that
imports an explicitly selected public Core checkout. It does not ship hooks,
installers, downloaders, binaries, credentials, or telemetry.

Skill instructions link only to public Let’s Infer product and runtime
repositories. They never require access to private workspace context.

## Contributing

Read [AGENTS.md](AGENTS.md), then run:

```bash
python3 tools/validate_skills.py
```

Let’s Infer agent skills are licensed under
[AGPL-3.0-only](LICENSE).
