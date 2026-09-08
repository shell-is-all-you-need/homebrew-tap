#!/usr/bin/env python3
"""Update the formula from the latest shell-is-all-you-need GitHub release."""

from __future__ import annotations

import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

REPOSITORY = "shell-is-all-you-need/mcp"
ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "mac_arm": "aarch64-apple-darwin",
    "mac_intel": "x86_64-apple-darwin",
    "linux_arm": "aarch64-unknown-linux-musl",
    "linux_intel": "x86_64-unknown-linux-musl",
}


def download(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "shell-is-all-you-need-homebrew-updater"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    release = json.loads(
        download(f"https://api.github.com/repos/{REPOSITORY}/releases/latest")
    )
    tag = release["tag_name"]
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise SystemExit(f"unsupported release tag: {tag}")
    version = tag.removeprefix("v")
    assets = {asset["name"]: asset["browser_download_url"] for asset in release["assets"]}

    values: dict[str, tuple[str, str]] = {}
    for key, target in TARGETS.items():
        name = f"shell-is-all-you-need-{target}"
        url = assets[name]
        checksum = download(assets[name + ".sha256"]).decode("ascii").split()[0]
        if not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise SystemExit(f"invalid checksum for {name}")
        values[key] = (url, checksum)

    def block(key: str, indent: str = "    ") -> str:
        url, checksum = values[key]
        return f'{indent}url "{url}", using: :nounzip\n{indent}sha256 "{checksum}"'

    formula = f'''class ShellIsAllYouNeed < Formula
  desc "Dependency-free multi-tool MCP server for fixed process invocations"
  homepage "https://shell-is-all-you-need.github.io/"
  version "{version}"
  license "MIT"

  on_macos do
    on_arm do
{block("mac_arm", "      ")}
    end
    on_intel do
{block("mac_intel", "      ")}
    end
  end

  on_linux do
    on_arm do
{block("linux_arm", "      ")}
    end
    on_intel do
{block("linux_intel", "      ")}
    end
  end

  def install
    bin.install Dir["shell-is-all-you-need-*"].first => "shell-is-all-you-need"
    chmod 0755, bin/"shell-is-all-you-need"
  end

  test do
    assert_match version.to_s, shell_output("#{{bin}}/shell-is-all-you-need --version")
  end
end
'''
    destination = ROOT / "Formula/shell-is-all-you-need.rb"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(formula, encoding="utf-8")
    print(f"Updated formula to {version}")


if __name__ == "__main__":
    main()
