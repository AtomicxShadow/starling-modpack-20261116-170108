#!/usr/bin/env python3
"""Check source integrity and bundle references; this does not compile Rust."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def inside(base, relative):
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError(f"Path outside bundle: {relative}")
    return path


def selected(value, known):
    ids = sorted(known) if value.strip() == "all" else value.replace(",", " ").split()
    if not ids or len(ids) != len(set(ids)) or set(ids) - set(known):
        raise ValueError(f"Choose all or distinct ids from: {', '.join(sorted(known))}")
    return sorted(ids)


def check_bundle(folder):
    data = tomllib.loads((folder / "horizon-mixin.toml").read_text())
    if data["mod"]["id"] != folder.name:
        raise ValueError(f"Bundle id differs from folder: {folder}")
    for section in ("module", "injection", "crate"):
        seen = set()
        for item in data.get(section, []):
            if item["id"] in seen:
                raise ValueError(f"Duplicate {section} id: {folder.name}/{item['id']}")
            seen.add(item["id"])
            key = {"module": "source", "injection": "helper", "crate": "path"}[section]
            path = inside(folder, item[key])
            required = path / "Cargo.toml" if section == "crate" else path
            if not required.is_file():
                raise ValueError(f"Missing bundle input: {required}")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--mods", default="all")
    args = parser.parse_args()
    lock = json.loads((ROOT / "sources.lock.json").read_text())
    ids = selected(args.mods, lock["mods"])
    for name in ids:
        folder = ROOT / "mixins" / name
        expected = lock["mods"][name]["files"]
        actual = {
            p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob("*") if p.is_file()
        }
        if actual != expected:
            raise ValueError(f"Sources differ from sources.lock.json: {name}")
        data = check_bundle(folder)
        print(f"Bundle references and hashes OK: {name} {data['mod']['version']}")
    if args.source:
        source = args.source.resolve()
        commit = subprocess.check_output(
            ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
        ).strip()
        if commit != lock["starling"]["commit"]:
            raise ValueError(f"Expected Starling {lock['starling']['commit']}, got {commit}")
        # Apply Starling's own adapter only to disposable bundle copies.
        spec = importlib.util.spec_from_file_location(
            "native_mod_adapt", source / "packaging/android/native_mod_adapt.py"
        )
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        modules = adapter.owners(source)
        with tempfile.TemporaryDirectory(prefix="starling-bundle-check-") as tmp:
            for name in ids:
                folder = Path(tmp) / name
                shutil.copytree(ROOT / "mixins" / name, folder)
                manifest = folder / "horizon-mixin.toml"
                manifest.write_text(adapter.adapt(manifest.read_text(), source, modules))
                data = check_bundle(folder)
                for module in data.get("module", []):
                    if not inside(source, module["file"]).is_file():
                        raise ValueError(f"Missing Starling module destination: {name}/{module['file']}")
        print(f"Starling commit and module destination files OK: {commit}")
    print("Static checks passed. Rust/AST compatibility and Android runtime remain unverified.")


if __name__ == "__main__":
    main()
