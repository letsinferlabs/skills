# Contributing

Changes should make a Let’s Infer workflow clearer or safer across all
supported agent harnesses.

1. Edit the smallest applicable skill.
2. Verify every product statement against the linked public Let’s Infer
   contract.
3. Keep privileged repository-maintainer procedures out of the public skills.
4. Run `python3 tools/validate_skills.py`.
5. Open a pull request describing the user request the change improves.

Do not add a new skill when an existing focused skill can route the request
without becoming ambiguous. Do not add harness-specific copies of the same
instructions; optional presentation metadata belongs under `agents/`.
