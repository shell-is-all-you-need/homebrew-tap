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
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.2/shell-is-all-you-need-aarch64-apple-darwin", using: :nounzip
      sha256 "26bb807315de911f0101a27a15661b829077259bd097d644a3694f447e2d9014"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.2/shell-is-all-you-need-x86_64-apple-darwin", using: :nounzip
      sha256 "6131430e0ce457e58f2bc0b5a248302cc8c941894474a03d387cccc05f19adbd"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.2/shell-is-all-you-need-aarch64-unknown-linux-musl", using: :nounzip
      sha256 "625abc4128c6da4b31994726686a7e1246f3c7b0022d29817204e9d0cb615f62"
    end
    on_intel do
      url "https://github.com/shell-is-all-you-need/mcp/releases/download/v0.1.2/shell-is-all-you-need-x86_64-unknown-linux-musl", using: :nounzip
      sha256 "661a291b1e5815af5b08dff5b4d584cc9852a996de73904709ea2ccf623220b0"
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
