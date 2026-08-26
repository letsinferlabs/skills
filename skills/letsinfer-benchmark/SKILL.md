---
name: letsinfer-benchmark
description: Design, run, resume, verify, audit, and report reproducible Let’s Infer runtime benchmarks. Use for context and concurrency matrices, TPS, TTFT, cache cold/warm/restart behavior, correctness, pressure, soak, telemetry, evidence hashes, or runtime pull-request verification.
---

# Benchmark a Let’s Infer runtime

Measure one exact runtime identity under its declared production recipe. Never
transfer evidence across a changed model or tokenizer revision, Engine OCI,
runtime pack, target, serving recipe, kernel/patch set, benchmark contract, or
cache format.

Read the current public sources before changing or interpreting a benchmark:

1. [benchmark framework](https://github.com/letsinferlabs/letsinfer/blob/main/benchmarks/README.md);
2. [canonical prompt protocol](https://github.com/letsinferlabs/letsinfer/blob/main/benchmarks/prompts/PROTOCOL.md); and
3. [CLI benchmark and verification commands](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/reference/cli.md#benchmark).

Prefer the local files when already working in the corresponding public Core
checkout.

## Choose the operation

### Measure an installed runtime

Inspect the selected model/runtime and list the declared benchmark cells before
running expensive inference:

```bash
letsinfer model list MODEL --installed --json
letsinfer benchmark list MODEL
letsinfer benchmark run MODEL
```

Use documented context and concurrency selectors only for a narrow diagnostic
or explicitly requested subset. A release qualification uses the complete
declared contract; do not shorten it or select favorable rows.

Benchmark jobs are durable. Ctrl-C detaches rather than cancelling. Use the
installed CLI help for attach/status behavior and `letsinfer benchmark stop`
to cancel and restore deliberately. Do not start a second benchmark while one
is active.

### Verify a runtime pull request

For a public runtime proposal that has passed the repository’s readiness gate:

```bash
letsinfer benchmark verification run <pull-request-url>
letsinfer benchmark verification status
letsinfer benchmark verification stop
```

Verification accepts no workload or recipe overrides. It resolves the exact
trusted-finalizer artifact for the current PR head, validates its identities
and attestations, compares it against the current baseline under the same
contract, and restores the verifier’s resident runtime on every terminal path.
It does not build arbitrary pull-request source.

Runtime authors may run the verifier for useful information, but they do not
turn their own result into independent qualification. Any accepted
correctness, safety, crash, OOM, incomplete-workload, or restoration failure is
blocking for that exact subject.

## Seal identity before measurement

Start from a clean named source revision and record:

- source commit and tree;
- runtime pack/descriptor and private execution-view identity;
- Engine OCI manifest and image configuration digests;
- model and tokenizer revisions;
- target and physical-device topology;
- arguments, environment, resource bounds, and serving capacity;
- benchmark contract, prompt generator/templates, materialized prompt-set
  hashes, request settings, and cache namespace; and
- comparison baseline with proof that its method is equivalent.

Use a new immutable evidence directory. Never overwrite, splice, average, or
combine evidence from different identities or lifecycle states.

## Preserve canonical prompts and execution

Let Core materialize the declared prompt suite. Count the complete rendered
request through the exact Engine adapter and record the real per-stream token
counts. Never resize canonical prompts with a tokenizer, reuse one prompt to
fake concurrency, or force output content to improve a result.

Obey the benchmark contract’s process and cache lifecycle. Cold per-cell,
shared-matrix, prefix-shared, short-concurrency, and cache-reload schemas are
different methods; do not compare or relabel them as equivalent. Reject a cell
that cannot fit its prompt plus output reserve rather than shortening it.

## Exercise qualification lanes

Run a narrow parity screen first when diagnosing a candidate, then the complete
declared qualification only after it passes. The full evidence should cover:

1. historical or predecessor parity for exactly comparable rows;
2. every declared context and concurrency cell;
3. output correctness, finish reasons, usage, and cache counters;
4. connection admission, active-request capacity, queueing, and too-large
   requests;
5. cold miss, immediate warm reuse, graceful restart, and restored reuse when
   persistent cache is declared;
6. corrupt/incompatible persistent records becoming misses;
7. pressure, protection, ordinary crash restart, OOM latch, recovery, and
   reboot persistence; and
8. the complete soak plan when the runtime contract requires one.

A failed correctness, safety, identity, cache, stability, or capacity gate is
not a slow result. Stop and repair that boundary before continuing.

## Capture complete evidence

Retain raw requests, streaming events, outputs, token/finish metadata, runtime
logs, and the structured result. Capture at least:

- prompt, completion, and cached tokens;
- TTFT, wall latency, decode TPS, and aggregate TPS;
- queue depth and active request state;
- CPU/GPU utilization, memory, temperature, power, and clocks;
- host memory, swap, PSI, cgroup OOM state, and NVMe I/O/temperature;
- container health, restart count, OOM state, and resource use; and
- Watchdog state, trip record, peak memory, and protection action.

Use the sampling intervals fixed by the runtime contract. Do not change
polling overhead between comparison arms. Keep private machine identifiers out
of public evidence and preserve the product’s hashed/pseudonymous identities.

## Decide and report

Report cold, warm, and restored behavior separately. Identify the exact
runtime/model/Engine/target subject, benchmark contract, evidence directory,
record hash, failures, and comparable baseline. Do not hide unavailable
metrics by writing zero or infer cache hits from timing when the Engine did not
report cached tokens.

Validate the generated benchmark record with the current Core tooling before
using it as evidence. Keep materialized prompts, complete outputs, and
machine-specific raw evidence in ignored evidence storage. Repository
automation, not an author or this skill, owns consensus and qualification
metadata.
