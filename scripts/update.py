#!/usr/bin/env python3
"""Update the formula from the latest shell-is-all-you-need GitHub release.

Usage: update.py [--dry-run]

With --dry-run the rendered formula is compared with the current one and
nothing is written. Set GITHUB_TOKEN to avoid anonymous API rate limits.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

sys.dont_write_bytecode = True

REPOSITORY = "shell-is-all-you-need/mcp"
ROOT = Path(__file__).resolve().parents[1]
FORMULA = ROOT / "Formula" / "shell-is-all-you-need.rb"
TARGETS = {
    "mac_arm": "aarch64-apple-darwin",
    "mac_intel": "x86_64-apple-darwin",
    "linux_arm": "aarch64-unknown-linux-musl",
    "linux_intel": "x86_64-unknown-linux-musl",
}
TEMPLATE = """class ShellIsAllYouNeed < Formula
  desc "Dependency-free multi-tool MCP server for fixed process invocations"
  homepage "https://shell-is-all-you-need.github.io/"
  license "MIT"

  livecheck do
    url :url
    strategy :github_latest
  end

  on_macos do
    on_arm do
@MAC_ARM@
    end
    on_intel do
@MAC_INTEL@
    end
  end

  on_linux do
    on_arm do
@LINUX_ARM@
    end
    on_intel do
@LINUX_INTEL@
    end
  end

  def install
    bin.install Dir["shell-is-all-you-need-*"].first => "shell-is-all-you-need"
    chmod 0755, bin/"shell-is-all-you-need"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/shell-is-all-you-need --version")
    assert_match "--tool", shell_output("#{bin}/shell-is-all-you-need --help")
  end
end
"""


def download(url: str) -> bytes:
    headers = {"User-Agent": "shell-is-all-you-need-homebrew-updater"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=60) as response:
        return response.read()


def parse_checksum(text: str, name: str) -> str:
    fields = text.split()
    if not fields or not re.fullmatch(r"[0-9a-f]{64}", fields[0]):
        raise SystemExit(f"invalid checksum for {name}")
    if len(fields) > 1 and fields[1].lstrip("*") != name:
        raise SystemExit(f"checksum file for {name} names {fields[1]!r}")
    return fields[0]


def render(tag: str, assets: dict[str, str]) -> str:
    prefix = f"https://github.com/{REPOSITORY}/releases/download/{tag}/"
    blocks: dict[str, str] = {}
    for key, target in TARGETS.items():
        name = f"shell-is-all-you-need-{target}"
        missing = [asset for asset in (name, name + ".sha256") if asset not in assets]
        if missing:
            raise SystemExit(f"release {tag} is missing asset(s): {', '.join(missing)}")
        url = assets[name]
        if not url.startswith(prefix):
            raise SystemExit(f"unexpected download URL for {name}: {url}")
        checksum = parse_checksum(
            download(assets[name + ".sha256"]).decode("ascii"), name
        )
        blocks[key] = f'      url "{url}", using: :nounzip\n      sha256 "{checksum}"'
    text = TEMPLATE
    for key, block in blocks.items():
        text = text.replace(f"@{key.upper()}@", block)
    return text


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(
        dir=path.parent, prefix=".formula-", suffix=".tmp"
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            file.write(text)
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--dry-run", action="store_true", help="report changes without writing"
    )
    arguments = parser.parse_args()

    release = json.loads(
        download(f"https://api.github.com/repos/{REPOSITORY}/releases/latest")
    )
    tag = release["tag_name"]
    if (
        not re.fullmatch(r"v\d+\.\d+\.\d+", tag)
        or release.get("draft")
        or release.get("prerelease")
    ):
        raise SystemExit(f"unsupported release: {tag}")
    assets = {
        asset["name"]: asset["browser_download_url"] for asset in release["assets"]
    }

    formula = render(tag, assets)
    current = FORMULA.read_text(encoding="utf-8") if FORMULA.exists() else None
    if current == formula:
        print(f"Formula already at {tag.removeprefix('v')}")
    elif arguments.dry_run:
        print(f"Would update formula to {tag.removeprefix('v')}")
    else:
        write_atomic(FORMULA, formula)
        print(f"Updated formula to {tag.removeprefix('v')}")


if __name__ == "__main__":
    main()
