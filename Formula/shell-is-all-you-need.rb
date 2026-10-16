class ShellIsAllYouNeed < Formula
  desc "Dependency-free multi-tool MCP server for fixed process invocations"
  homepage "https://shell-is-all-you-need.github.io/"
  license "MIT"

  livecheck do
    url :url
    strategy :github_latest
  end

  on_macos do
    on_arm do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.2.0/shell-is-all-you-need-aarch64-apple-darwin", using: :nounzip
      sha256 "5e2ed484c6cb6907106aba92935d45e1c0fcabfe1ba1cc4fe1cf19c60fabeb0c"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.2.0/shell-is-all-you-need-x86_64-apple-darwin", using: :nounzip
      sha256 "ff18e356f58f2f4e16673da87e67eeb62634bc4dc61ad1161b2ebc734ce1914d"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.2.0/shell-is-all-you-need-aarch64-unknown-linux-musl", using: :nounzip
      sha256 "dc2a88af87a935af2cd219480b5e73b946b4fbb49fe491628fa7777187abb1a0"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.2.0/shell-is-all-you-need-x86_64-unknown-linux-musl", using: :nounzip
      sha256 "c7937703e7f9a781fe05b5b26b922e897e07b246f231b66f4f10f4d4528fb9ce"
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
