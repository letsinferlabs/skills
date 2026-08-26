---
name: letsinfer-runtime-authoring
description: Create, port, optimize, and qualify a Let’s Infer runtime candidate that binds an exact model, immutable Engine OCI, hardware target, serving recipe, cache contract, and benchmark plan. Use for candidate source in letsinferlabs/runtimes; use letsinfer-engine-authoring as well when Engine executable inputs change.
---

# Author a Let’s Infer runtime

Create one reproducible candidate without moving model- or Engine-specific
behavior into Core. Work in the public
[runtimes repository](https://github.com/letsinferlabs/runtimes).

Before editing, read the current public contracts:

1. [runtime format](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/reference/runtime-format.md);
2. [runtime candidates](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/concepts/runtime-packs.md);
3. [Engine boundary](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/concepts/engine-adapters.md); and
4. [runtimes contributor workflow](https://github.com/letsinferlabs/runtimes/blob/main/CONTRIBUTING.md).

When those repositories are already checked out, prefer their local files so
the instructions match the code revision being changed.

## Recover the starting identity

Before optimizing or porting, record the exact prior model and tokenizer
revision, runtime version, Engine OCI manifest, configuration, and execution
payload digests, upstream Engine version, target, arguments, environment, context/capacity
envelope, cache lifecycle, benchmark contract, and comparable evidence. Never
compare or transfer evidence across a changed identity.

## Choose the candidate form

Every candidate is one flat top-level directory:

```text
<engine>--<lowercase-hf-owner>--<lowercase-hf-model>--<target>/
```

The directory name and `runtime.id` must match. It contains `runtime.json`,
`release.json`, and `README.md`, plus only the source needed by that candidate.
Do not add nested model/Engine/target trees or a second execution manifest.

Classify the Engine path before editing:

- **Reuse Engine:** preserve the exact existing Engine manifest,
  configuration, and execution-payload digests. Omit `adapter/`, `engine/`,
  and `image/`; do not copy
  an unchanged Engine merely because a new runtime uses it.
- **Change or add Engine:** include the complete Engine source or immutable
  acquisition, adapter, deterministic image recipe, patches, kernels, tests,
  licenses, and notices in this same candidate. Also use the
  `letsinfer-engine-authoring` skill when it is installed.

Do not commit model weights, generated binaries, image layers, build caches,
OCI archives, credentials, or local benchmark evidence. Git retains reviewed
source; registries retain immutable deployable objects.

## Pin the model and Engine

Declare the primary `hf://owner/repository` and exact immutable revision.
Declare each required artifact, including exact filename and SHA-256 where the
format requires it. The runtime must acquire all model files itself; operators
do not preinstall weights or populate a runtime-specific model cache.

Pin the Engine by OCI manifest digest, image configuration digest, and
normalized execution-payload digest. Keep tokenizer behavior, exact token
counting, parsers, native Engine options,
Engine telemetry, cache integration, patches, and compiled kernels outside
Core. Never use a runtime-defined `LETSINFER_*` environment name.

Changing the Engine execution payload, model revision, recipe,
behavior-bearing kernel/patch, or cache format creates a new qualification
subject. Packaging-only OCI changes preserve evidence when the payload digest
is unchanged; benchmark records retain the measured OCI digest for traceability.

## Define the measured target and recipe

Publish one serving recipe for one capability-based target. Declare platform,
accelerator architecture, device count/partitioning, memory topology and
minimum, container limits, context, connection and active-request capacity,
cache behavior, safety floor, and the benchmark contract measured together.
Never silently fall back to another checkpoint, quantization, Engine,
attention backend, kernel, cache format, or recipe.

Use `target.placement.strategy: single` for an independent Engine group. Core
may replicate that group unchanged. Use `parallel` only when the runtime
qualifies the complete multi-device or multi-node topology. The runtime owns
ranks, stages, collectives, rendezvous, and Engine flags; Core receives only
generic `task-N` assignments, phased lifecycle, bounded resources, readiness,
and one complete-group endpoint.

## Treat persistent cache as a contract

If the Engine supports safe persistent inference-state restore, use Core’s
provided `LETSINFER_CACHE_ROOT` and keep the provider/format in the Engine OCI.
Bind records to every replay-sensitive identity; commit atomically; validate
lengths, checksums, and compatibility; treat incomplete, corrupt, stale, or
incompatible records as misses; and enforce bounded capacity plus TTL.

If safe restore is unavailable, declare it non-persistent and document that
limit. Do not describe process-local prefix reuse as restored NVMe cache.

## Generate README and metadata

Root `release.json` uses the current publication schema, a non-empty ordered
authors array, the SPDX license, and unmaterialized automation-owned
provenance.

Attribute the runtime implementation, including materially derived work:

- Inspect the candidate’s Git history, upstream repository and pull requests,
  carried patches/kernels/recipes, source headers, and license/notices before
  choosing authors. Do not infer authorship only from the current submitter or
  the last commit.
- Include the identifiable people or organizations whose runtime-specific
  implementation is materially incorporated: original recipe or integration
  authors first, followed by downstream authors who adapted, ported, or added
  substantial behavior. Preserve that order across releases.
- Preserve an existing author while their material contribution remains in the
  candidate. Append a new material contributor; do not replace the upstream
  author with the person who ported or submitted the derived work. Remove an
  author only when their contribution is no longer present, and explain that
  lineage change in the pull request.
- Do not list a model/checkpoint author merely because the runtime downloads
  their weights. Link and pin the model as required, but list them as a runtime
  author only when their serving implementation, recipe, patch, or equivalent
  runtime work is actually incorporated.
- Benchmark verifiers, reviewers, sponsors, and repository maintainers are not
  runtime authors unless they also contributed material runtime source or
  design used by the candidate.
- Record each author’s current visible GitHub login, immutable numeric GitHub
  ID, and actual account type. Verify the identity through GitHub; never guess
  an ID, convert a person into an organization for convenience, or use a
  mutable display name.
- `release.json.authors` is a concise runtime-authorship list, not a substitute
  for copyright and dependency attribution. Preserve every upstream LICENSE,
  NOTICE, copyright, and source-link obligation in the candidate even when a
  dependency’s full contributor list does not belong in `authors`.

Do not add role or derivation fields that the publication schema does not
define. Put helpful acknowledgements and derived-source links in the README or
notices, while keeping the structured `authors` identities schema-valid. Do
not hand-author consensus, provenance, qualification status, or the generated
root catalog.

Generate the candidate README’s canonical Let’s Infer installation block:

```bash
python3 tools/readme_onboarding.py --candidate <candidate> --write
```

Preserve existing README content below that block. Link every declared Hugging
Face repository and include an exact reproduction command that matches the
candidate’s current qualification state.

## Validate locally

Use the tools from the checked-out runtimes repository. Runtime development is
deliberately absent from the product CLI; do not add or depend on a
`letsinfer runtime ...` command family.

```bash
python3 tools/readme_onboarding.py --candidate <candidate> --write
python3 tools/candidate_policy.py audit \
  --candidate <candidate> --mode <reuse-engine|build-engine>
# For build-engine only:
python3 tools/build_engine.py --candidate <candidate> --output /tmp/engine.oci.tar --pin
python3 tools/generate_manifest.py --validate-only
python3 -m unittest discover -s tests -p 'test_*.py'
```

For local deterministic pack validation, read
[runtime pack development](references/runtime-pack.md) and use the skill’s
helper with the exact checked-out Core revision; it packs unchanged source
twice and requires byte-identical runtime packs. Verify every external model
and image input is immutable. For a changed Engine, use the single canonical
Engine build above, then run candidate-specific tests and protocol conformance
before requesting runtime verification.

## Qualify the exact proposal

Open one pull request changing one candidate. Do not include generated
consensus, provenance, registry credentials, or publication output. Repository
automation audits and finalizes the exact proposal artifact without granting
contributors production credentials.

After the public source and supply-chain gate marks the proposal ready,
independent users run:

```bash
letsinfer benchmark verification run <pull-request-url>
```

Any accepted correctness, safety, OOM, crash, incomplete-workload, or
restoration failure is blocking for those exact bytes. Authors do not turn
their own local result into qualification. Once the public verification and
repository checks are satisfied, repository maintainers handle publication
and merge; the authoring skill does not perform or describe privileged release
authorization.
