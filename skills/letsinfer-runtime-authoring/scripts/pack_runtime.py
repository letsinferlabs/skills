#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
"""Pack one runtime twice through an exact checked-out Core contract."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import sys
import tempfile


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--core",
        required=True,
        type=pathlib.Path,
        help="path to the exact letsinferlabs/letsinfer checkout",
    )
    parser.add_argument("--candidate", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    return parser.parse_args()


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    values = arguments()
    core = values.core.resolve(strict=True)
    candidate = values.candidate.resolve(strict=True)
    if not (core / "core/runtime_packs.py").is_file():
        raise SystemExit("--core is not a Let’s Infer Core checkout")
    if not (candidate / "runtime.json").is_file():
        raise SystemExit("--candidate has no runtime.json")
    output = values.output.expanduser().resolve(strict=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(core))
    from core.runtime_packs import RuntimePackError, build_archive

    with tempfile.TemporaryDirectory(prefix="letsinfer-runtime-pack-") as temporary:
        root = pathlib.Path(temporary)
        first = root / "first.letsinfer"
        second = root / "second.letsinfer"
        try:
            first_pack = build_archive(candidate, first)
            second_pack = build_archive(candidate, second)
        except RuntimePackError as error:
            raise SystemExit(str(error)) from error
        first_digest = sha256(first)
        second_digest = sha256(second)
        if (
            first_digest != second_digest
            or first.read_bytes() != second.read_bytes()
            or first_pack.digest != second_pack.digest
        ):
            raise SystemExit("runtime pack is not byte-for-byte deterministic")
        with tempfile.NamedTemporaryFile(
            prefix=f".{output.name}.",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as handle:
            temporary_output = pathlib.Path(handle.name)
        try:
            shutil.copyfile(first, temporary_output)
            temporary_output.replace(output)
        finally:
            temporary_output.unlink(missing_ok=True)
    print(
        f"runtime={first_pack.runtime['id']} "
        f"version={first_pack.runtime['version']} "
        f"sha256={first_digest} bytes={output.stat().st_size} output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
