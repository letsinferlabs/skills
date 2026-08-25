---
name: letsinfer-engine-authoring
description: Develop a changed or entirely new inference Engine inside a Let’s Infer runtime candidate, including its protocol adapter, deterministic OCI recipe, telemetry translation, immutable inputs, tests, and local reproducibility. Use only when Engine executable inputs change; do not use for a runtime that reuses an unchanged Engine OCI.
---

# Author a Let’s Infer Engine

Use this skill when a runtime changes Engine internals or introduces an Engine
Let’s Infer does not yet support. Keep the Engine and runtime in one candidate
pull request; authors do not need preliminary registry publication.

Read the current public contracts before editing:

1. [Engine OCI and adapter protocol](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/concepts/engine-adapters.md);
2. [runtime format](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/reference/runtime-format.md); and
3. [runtimes contributor workflow](https://github.com/letsinferlabs/runtimes/blob/main/CONTRIBUTING.md).

If you are already in a matching public checkout, prefer its local files. Use
the `letsinfer-runtime-authoring` skill as well when it is installed; this
skill covers only the Engine-specific closure.

## Preserve the boundary

Core remains model- and Engine-agnostic. An Engine OCI combines one upstream
Engine version with the matching adapter and implements the current stable
Engine protocol. A new Engine does not require a Core change while that
protocol can express its inference, lifecycle, health, exact token counting,
telemetry, and generic resource needs.

Propose a protocol change only for a capability that is genuinely shared
across Engines. Keep upstream flags, tokenizer behavior, cache APIs, parsers,
rank/stage layout, collectives, rendezvous, and Engine-specific metrics in the
candidate and Engine OCI.

## Keep the complete source closure

Place all behavior-bearing inputs in the runtime candidate:

- complete Engine source or immutable source acquisition;
- matching protocol adapter;
- digest-pinned base images and deterministic image recipe;
- patches, plugins, kernels, and build configuration;
- target-specific tests and protocol fixtures;
- inventory/SBOM inputs, licenses, copyrights, and notices.

Pin every remote input by digest or cryptographic hash. Do not commit model
weights, generated binaries, container layers, build caches, OCI archives,
credentials, or local benchmark evidence. Do not require contributors to log
in to a production registry.

## Implement the protocol adapter

The image exposes the fixed adapter executable documented by the current
Engine protocol. It must provide:

- OpenAI-compatible inference;
- health and served-model identity;
- exact Engine-rendered chat token counting; and
- normalized request, queue, token, context, prefix-cache, and KV-cache
  telemetry required by the protocol.

The adapter is the telemetry hook into radical Engine internals. Translate
native counters and state at this boundary. Report unavailable optional values
as unavailable, never as zero. Do not add Engine-specific probes, flags,
ranks, or schemas to Core.

Protect Core-owned listeners, mounts, credentials, authentication, admission,
safety, and protocol values from runtime overrides. Treat a protocol-owned
environment name or argument as reserved.

## Build deterministically without publishing

Use the checked-out runtimes repository’s candidate audit, Docker/buildx,
inventory, OCI inspection, and packing tools. Build only local images or OCI
layouts outside Git. Exercise the declared target architecture rather than
transferring an image or result from another platform.

Required local evidence includes:

1. adapter protocol conformance in the exact image;
2. exact model and tokenizer identity plus rendered token counting;
3. health and normalized telemetry capture/replay;
4. admission and structured too-large-request behavior;
5. ordinary restart, process crash, pressure, OOM, and protection behavior;
6. proof that runtime inputs cannot replace protocol-owned values; and
7. two builds from unchanged inputs with identical OCI identity and package
   inventory.

Perturb irrelevant build state such as checkout timestamps when testing
reproducibility. A deterministic result must derive from source inputs, not an
accidentally shared cache. Build output and package inventory remain temporary
artifacts.

Calculate the future Engine manifest and image configuration digests with the
repository tools and pin them in `runtime.json`. This calculation is local and
does not publish an OCI. Repository automation independently checks the exact
source identity and will reject a differing pin.

## Cache and telemetry

When the Engine exposes safe persistent inference-state hooks, implement the
provider and format in the Engine OCI and use the Core-provided cache root.
Bind safe replay to model/tokenizer, Engine OCI, format/ABI, tensor layout and
dtype, attention backend, relevant kernels, and rendered prompt tokens.

Validate records before restore, write atomically, treat corrupt or
incompatible state as a miss, and enforce capacity plus TTL. Qualification
must distinguish process-local warm reuse from post-restart persistent reuse.

## Submit one reviewable runtime proposal

Submit the complete Engine and runtime source together. Repository automation
rebuilds and finalizes the exact proposal without exposing registry
credentials to candidate code. Verifiers benchmark that finalized artifact,
not an arbitrary locally published image.

Once source, protocol, reproducibility, benchmark, and repository checks are
satisfied, repository maintainers handle publication and merge. Do not publish
an unofficial production Engine, create package visibility, or describe
privileged release authorization in contributor instructions.
