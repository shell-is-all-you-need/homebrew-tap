# Homebrew tap

Homebrew formula for [shell-is-all-you-need](https://shell-is-all-you-need.github.io/), a dependency-free MCP server that turns fixed process invocations into tools.

```sh
brew install shell-is-all-you-need/tap/shell-is-all-you-need
```

Or add the tap first and use the short name:

```sh
brew tap shell-is-all-you-need/tap
brew install shell-is-all-you-need
```

The formula installs the prebuilt release binary for ARM64 and x86-64 on macOS and Linux (musl static binaries on Linux), and verifies its SHA-256 checksum.

## Maintenance

`.github/workflows/update.yml` runs every six hours, reads the latest non-prerelease GitHub release of `shell-is-all-you-need/mcp`, validates the four platform assets and their `.sha256` files, and commits the regenerated formula.

```sh
python3 -I scripts/update.py --dry-run   # report whether an update is needed, write nothing
python3 -I scripts/update.py             # rewrite Formula/shell-is-all-you-need.rb
brew style Formula/shell-is-all-you-need.rb
brew audit --strict --formula shell-is-all-you-need/tap/shell-is-all-you-need
```

Do not edit the formula by hand; change the template in `scripts/update.py`. Set `GITHUB_TOKEN` to avoid anonymous API rate limits.
