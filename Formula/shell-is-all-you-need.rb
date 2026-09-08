class ShellIsAllYouNeed < Formula
  desc "Dependency-free multi-tool MCP server for fixed process invocations"
  homepage "https://shell-is-all-you-need.github.io/"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.0/shell-is-all-you-need-aarch64-apple-darwin", using: :nounzip
      sha256 "7f7b84a903cb5b41d3f5fd45a84142a22c8055f0cb0baeef7137c71877b61eb2"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.0/shell-is-all-you-need-x86_64-apple-darwin", using: :nounzip
      sha256 "b77876bd11e5003ba924639f62df811e2e1af97e2af331410b87fa9df9a19e19"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.0/shell-is-all-you-need-aarch64-unknown-linux-musl", using: :nounzip
      sha256 "a97b16ebaacfd6b013a12fa5a85ac354cc61bed352376b06e523e74109b57928"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.0/shell-is-all-you-need-x86_64-unknown-linux-musl", using: :nounzip
      sha256 "46fbac99b4dd5175cfe238e3cb101f78d4400f167f2fd4159de51dc201bbfb70"
    end
  end

  def install
    bin.install Dir["shell-is-all-you-need-*"].first => "shell-is-all-you-need"
    chmod 0755, bin/"shell-is-all-you-need"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/shell-is-all-you-need --version")
  end
end
