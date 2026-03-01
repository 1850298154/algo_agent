"""Test MCP stdio connection for vision_mcp server."""
import subprocess
import json
import sys


def test_mcp_stdio():
    """Test if the MCP server can communicate via stdio."""
    print("Starting MCP server test...")
    print("=" * 50)

    # Start the MCP server
    proc = subprocess.Popen(
        [sys.executable, "-m", "vision_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Send initialize request
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }

    print("Sending initialize request...")
    proc.stdin.write(json.dumps(initialize_request) + "\n")
    proc.stdin.flush()

    # Try to read response
    try:
        response = proc.stdout.readline()
        if response:
            print(f"Response: {response[:200]}...")
            print("\n✓ MCP stdio communication works!")
            return True
        else:
            print("\n✗ No response received")
            return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    success = test_mcp_stdio()
    sys.exit(0 if success else 1)
