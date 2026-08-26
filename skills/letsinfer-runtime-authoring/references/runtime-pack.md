# Runtime pack development

Use the runtime-authoring skill’s helper to exercise the exact Core packing
contract without adding development commands to the product CLI:

```bash
python3 skills/letsinfer-runtime-authoring/scripts/pack_runtime.py \
  --core /path/to/letsinferlabs/letsinfer \
  --candidate <candidate> \
  --output /tmp/runtime.letsinfer
```

Pin `--core` to the exact public Core revision used by the runtimes repository
verification contract. The helper imports `core.runtime_packs.build_archive`,
packs the candidate twice in isolated temporary paths, requires byte-for-byte
equality and matching descriptor digests, and atomically writes only the final
artifact.

The candidate source remains the complete review unit. Do not copy the pack
implementation into the skill, hand-edit a generated archive, publish local
pack output, or treat a successful local pack as qualification evidence.

Local pack artifacts are temporary validation output. Keep them outside Git
and let trusted repository automation finalize, attest, and publish the exact
reviewed proposal.
