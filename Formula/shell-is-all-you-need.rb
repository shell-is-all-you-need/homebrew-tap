class ShellIsAllYouNeed < Formula
  desc "Dependency-free multi-tool MCP server for fixed process invocations"
  homepage "https://shell-is-all-you-need.github.io/"
  version "0.1.1"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.1/shell-is-all-you-need-aarch64-apple-darwin", using: :nounzip
      sha256 "4eb2b285334b9ec59b8ca4979d9857fbf9c49fc4f39789ae90984a5b13ac91bd"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.1/shell-is-all-you-need-x86_64-apple-darwin", using: :nounzip
      sha256 "ace3eb6d014e0554c21e5f0e8829a59903b9ddb83dabb5316fae4ddd95eba940"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.1/shell-is-all-you-need-aarch64-unknown-linux-musl", using: :nounzip
      sha256 "d771262cd3b01a2cc0410eecabc8a011948219107e6c4eeb3229dfd41104e30d"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.1/shell-is-all-you-need-x86_64-unknown-linux-musl", using: :nounzip
      sha256 "be1061a186afa4cc52c9e4e5bebf0b06e3f6b9e61113e4248d8a210fb7bd2e94"
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
