"""Tests for the Pedestal add-on that do not need Blender."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pedestal import parse_args


def test_parse_args_minimum():
    args = parse_args(["pedestal.py", "--", "/tmp/out", "--height", "0.6"])
    assert args.out == Path("/tmp/out")
    assert args.height == 0.6
    assert args.width == 0.4
    assert args.steps == 3


def test_parse_args_all():
    args = parse_args(["pedestal.py", "--", "out", "--height", "1.0", "--width", "0.5", "--steps", "5"])
    assert args.height == 1.0
    assert args.width == 0.5
    assert args.steps == 5


def test_manifest_is_valid_json_with_required_fields():
    manifest = json.loads(Path("addon.json").read_text(encoding="utf-8"))
    required = {"schema", "id", "name", "version", "author", "licence", "summary", "tools"}
    assert required <= set(manifest.keys())
    assert manifest["schema"] == 1
    assert manifest["id"] == "pedestal"
    assert manifest["tools"][0]["id"] == "build"
    assert "{out}" in manifest["tools"][0]["run"]
    assert "{blender}" in manifest["tools"][0]["run"]
