---
name: letsinfer-cli
description: Operate and troubleshoot the Let’s Infer CLI for node setup, signed model installation, serving, replication, status, API keys, updates, runtime upgrades, rollback, recovery, and removal. Use for an installed Let’s Infer system, not for authoring a new runtime candidate.
---

# Operate Let’s Infer

Use the installed `letsinfer` command and the exact help for that installed
version. Before constructing a command, read the current public
[CLI reference](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/reference/cli.md).
If you are already working in a checkout of `letsinferlabs/letsinfer`, prefer
that checkout’s `documentation/reference/cli.md` so code and documentation use
the same revision.

## Preserve the product model

- Users install a model with `letsinfer install MODEL`.
- The signed catalog and detected hardware select the recommended qualified
  runtime. There is no user-facing Engine selector.
- `--runtime CANDIDATE_ID` is an explicit exact-candidate override.
- `letsinfer update` changes Core only. `letsinfer upgrade MODEL` changes that
  model’s runtime only. Neither silently changes the other.
- Use the public topology terms **node**, **main**, and **child**. Do not expose
  retired topology vocabulary.
- Core owns replication and generic allocation. A runtime owns its Engine
  configuration and any TP/PP or other parallel execution semantics.

## Inspect before changing state

Start with the narrowest useful read-only commands:

```bash
letsinfer node status
letsinfer hardware --json
letsinfer status --json
letsinfer doctor --json
letsinfer update check
```

Use `letsinfer COMMAND --help` before relying on an option not shown in the
public reference. Prefer `--json` for automation; human presentation may
evolve.

Never place API keys, pairing material, registry credentials, or private
machine details in commands, source, logs, or benchmark evidence. Do not
weaken catalog signatures, immutable model/OCI pins, target compatibility,
admission, or Watchdog protection to make an operation pass.

## Route the request

### Set up and inspect nodes

Use `letsinfer setup` for the first machine. It becomes the main node. Use
`node`, `topology`, and `child` commands from the installed help to inspect or
manage additional nodes. Confirm the command’s printed `main`, `child`, or
`all` execution scope before mutating topology or access state.

### Discover and install a model

```bash
letsinfer list
letsinfer list MODEL --versions
letsinfer install MODEL
```

For replication, let interactive install propose compatible nodes or use the
documented `--node`, `--all-nodes`, and `letsinfer scale MODEL --replicas N`
controls. Review incompatibilities and replacement impact before using
`--replace-existing`.

### Inspect and control serving

Use `status`, `runtimes`, `inspect`, `verify`, `doctor`, and `logs` to establish
the exact model, runtime pack, Engine OCI, target, service, gateway, and
Watchdog state. Use `start`, `restart`, or `stop` only after inspection.

A protection trip is not an ordinary stopped service. Inspect the trip and its
cause; use `recover` only as the explicit acknowledgement path after the cause
is addressed. Do not use start or restart to erase safety history.

### Manage access

Create, list, rotate, and revoke API keys through `letsinfer key`. Key mutation
is main-node authority, and secret material is shown once. Verify the stable
OpenAI-compatible gateway after any access change without printing secrets.

### Update, upgrade, and roll back

```bash
letsinfer update check
letsinfer update
letsinfer upgrade MODEL --dry-run
letsinfer upgrade MODEL
letsinfer rollback MODEL --dry-run
letsinfer rollback MODEL
```

An upgrade is explicit and model-tied. For a recommended installation, a newer
qualified version of the same candidate or a different compatible recommended
candidate can be offered. Exact, digest-pinned, and local selections remain
subject to their recorded pin policy. The new runtime must stage and verify
before it replaces the active service; a failed activation must retain or
restore the prior immutable runtime.

### Benchmark

For ordinary measurement or runtime PR verification, use the separately
installed `letsinfer-benchmark` skill when available. Never start a second
benchmark while one is active. Ctrl-C detaches from a durable benchmark; it
does not cancel it.

### Remove Let’s Infer

`letsinfer uninstall` is destructive and requires explicit user intent.
`--keep-models` preserves only model storage. Inspect the installed help and
confirm the requested data boundary before proceeding.

## Verify the outcome

After a mutation, re-read machine-readable state and verify the intended
identity rather than trusting a successful process exit alone. Check the
launcher, user services, gateway/API, model revision, runtime pack, Engine OCI,
target, Watchdog state, and any affected node topology.
