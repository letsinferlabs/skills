---
name: letsinfer-cli
description: Operate and troubleshoot the Let’s Infer CLI for nodes, live topology, signed model installation, serving, status, authentication, updates, rollback, recovery, and removal. Use for an installed Let’s Infer system, not for authoring a runtime candidate.
---

# Operate Let’s Infer

Use the installed `letsinfer` command and the exact help for that installed
version. Before constructing a command, read the current public
[CLI reference](https://github.com/letsinferlabs/letsinfer/blob/main/documentation/reference/cli.md).
If you are already working in a checkout of `letsinferlabs/letsinfer`, prefer
that checkout’s `documentation/reference/cli.md` so code and documentation use
the same revision.

## Preserve the product model

- Users install a model with `letsinfer model install MODEL`.
- The signed catalog and detected hardware select the recommended qualified
  runtime. There is no user-facing Engine selector.
- `--runtime CANDIDATE_ID` is an explicit exact-candidate override.
- `letsinfer update core` changes Core only. `letsinfer update model MODEL` changes that
  model’s runtime only. Neither silently changes the other.
- Use the public topology terms **node**, **main**, and **child**. Do not expose
  retired topology vocabulary.
- Core owns replication and generic allocation. A runtime owns its Engine
  configuration and any TP/PP or other parallel execution semantics.

## Inspect before changing state

Start with the narrowest useful read-only commands:

```bash
letsinfer node info --json
letsinfer node list --json
letsinfer topology --json
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

The installer initializes the first machine as the main node. Use `node info`,
`node list`, and the unified `node add` workflow to inspect or add machines;
use `node pause`, `node resume`, and `node remove` for maintenance. Confirm the
printed `main` or `all` execution scope before mutating node state.

`node info [NODE]`, `node pause [NODE]`, `node resume [NODE]`, and `node remove
[NODE]` accept an explicit member ID/name or open a role-aware interactive
selector. On a child, show the Coordinator context; the child may pause,
resume, or remove only itself through authenticated requests to the main. On a
main, include the main for pause/resume and children for remove. Preserve
interactive warnings for self/main pause and every removal; use explicit
targets and `--yes` for intended automation.

In `node add`, the main selects a certificate-pinned candidate and the
candidate accepts that exact request locally. That paired intent activates the
child directly; do not ask for or invent a second comparison-code step.
When `node add` runs on a child, it is the interactive detach entry point: the
user confirms leaving the current main, the main removes the authenticated
child, local standalone authority is created rollback-safely, and discovery
continues in the same command. Do not substitute a local-only identity reset
that would leave a ghost child on the main.

### Inspect live topology

Run `letsinfer topology` on the main node for the animated authenticated
membership tree, or use `letsinfer topology --json` for one stable snapshot.
The live view labels each child's actual control-network transport and keeps
verified direct-link capacity, RDMA/MTU facts, Watchdog host RX/TX traffic, and
model placement distinct; it never claims that host-wide traffic is a per-link
byte counter. The grey-to-white membership pulse is presentation only and must
not be interpreted as measured link traffic. Membership and online/offline
state refresh continuously; interface facts publish every second and verified
direct-link evidence refreshes every two seconds.

Topology evidence is renewed deterministically by the node agent. Do not look
for or invent manual topology probe, plan, or link-test commands. Live signed
interface facts trigger bounded certificate-verified ConnectX probes in both
directions, so connecting or disconnecting the cable adds or expires the
direct-link view without an operator command.

### Discover and install a model

```bash
letsinfer model list
letsinfer model list MODEL --versions
letsinfer model install MODEL
```

Omit `MODEL` to use the interactive node/model matrix. Assigning the same model
to multiple nodes creates replicas automatically; review incompatibilities and
replacement impact before using `--replace-existing`.

### Inspect and control serving

Use `status`, `doctor`, `model list`, and `model logs MODEL` to establish the
exact model, runtime pack, Engine OCI, target, service, gateway, and Watchdog
state. Use `model pause`, `model resume`, or `model restart` only after
inspection.

A protection trip is not an ordinary stopped service. Inspect the trip and its
cause; use `model recover MODEL` only as the explicit acknowledgement path
after the cause is addressed. Do not use resume or restart to erase safety
history.

### Manage access

Create, list, rotate, and revoke API keys through `letsinfer auth key`. Key mutation
is main-node authority, and secret material is shown once. Verify the stable
OpenAI-compatible gateway after any access change without printing secrets.

### Update, upgrade, and roll back

```bash
letsinfer update check
letsinfer update core
letsinfer update model MODEL --dry-run
letsinfer update model MODEL
letsinfer model rollback MODEL --dry-run
letsinfer model rollback MODEL
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
