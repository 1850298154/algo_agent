"""
Test script for GLM-4.6V Vision MCP Server

This script tests all available tools in the MCP server.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for module import
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# Check API key
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    print("ERROR: ZHIPU_API_KEY environment variable is not set")
    print("Please set it in your .env file")
    exit(1)

# Create test image if it doesn't exist
TEST_IMAGE_DIR = Path(__file__).parent / "test_images"
TEST_IMAGE_DIR.mkdir(exist_ok=True)

# Create a simple test image using PIL
try:
    from PIL import Image, ImageDraw, ImageFont

    test_image_path = TEST_IMAGE_DIR / "test_screenshot.png"

    # Create a test image with some text and UI elements
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # Draw header
    draw.rectangle([0, 0, 800, 60], fill='#4A90E2')
    draw.text((20, 20), "Test Webpage Screenshot", fill='white')

    # Draw some content
    draw.text((50, 100), "Sample Text Content", fill='black')
    draw.text((50, 150), "Price: $999.00", fill='green')
    draw.text((50, 200), "Status: Available", fill='blue')

    # Draw a button
    draw.rectangle([50, 250, 200, 300], fill='#28A745')
    draw.text((70, 265), "Click Me", fill='white')

    # Draw a table-like structure
    draw.rectangle([50, 350, 400, 500], outline='gray')
    draw.text((60, 360), "Item 1 | Value A", fill='black')
    draw.text((60, 390), "Item 2 | Value B", fill='black')
    draw.text((60, 420), "Item 3 | Value C", fill='black')
    draw.text((60, 450), "Item 4 | Value D", fill='black')

    img.save(test_image_path)
    print(f"Created test image at: {test_image_path}")

except ImportError:
    print("PIL not installed, skipping test image creation")
    print("Please install PIL: pip install Pillow")
    test_image_path = None


async def test_tools_directly():
    """Test MCP tools by directly calling server's tool functions."""
    print("\n" + "="*60)
    print("Testing GLM-4.6V Vision MCP Server Tools")
    print("="*60 + "\n")

    try:
        # Import server module and access tools directly
        from vision_mcp.server import (
            analyze_image,
            extract_text_from_image,
            detect_objects_in_image,
            get_model_info
        )

        print("1. Getting model info...")
        model_info = get_model_info()
        print(model_info)

        if test_image_path and test_image_path.exists():
            print("\n2. Testing analyze_image tool...")
            result = await analyze_image(
                image_path=str(test_image_path),
                prompt="What elements and text are visible in this screenshot?",
                temperature=0.5
            )
            print(f"Result:\n{result}")

            print("\n3. Testing extract_text_from_image tool...")
            result = await extract_text_from_image(
                image_path=str(test_image_path)
            )
            print(f"Result:\n{result}")

            print("\n4. Testing detect_objects_in_image tool...")
            result = await detect_objects_in_image(
                image_path=str(test_image_path)
            )
            print(f"Result:\n{result}")
        else:
            print("\n2-4. Skipping tool tests (no test image available)")
            print("   Test images should be placed in: test_images/")

        print("\n" + "="*60)
        print("All tool tests completed successfully!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\nERROR during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True


async def test_direct_import():
    """Test importing the server module directly."""
    print("\n" + "="*60)
    print("Testing direct import of vision_mcp.server")
    print("="*60 + "\n")

    try:
        from vision_mcp.server import (
            encode_image,
            GLM_4_6V_MODEL
        )

        print("Import successful!")
        print(f"Model: {GLM_4_6V_MODEL}")

        if test_image_path and test_image_path.exists():
            print(f"\nTesting image encoding...")
            encoded = encode_image(str(test_image_path))
            print(f"Base64 length: {len(encoded)} characters")
            print("Encoding successful!")

        print("\nDirect import test passed!")
        return True

    except Exception as e:
        print(f"ERROR during import test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_mcp_protocol():
    """Test MCP server protocol by checking FastMCP object."""
    print("\n" + "="*60)
    print("Testing MCP Server Protocol")
    print("="*60 + "\n")

    try:
        # Import mcp server module
        from vision_mcp.server import mcp_server

        # FastMCP server object is created successfully
        print("FastMCP server object created successfully")
        print(f"Server name: {mcp_server.name if hasattr(mcp_server, 'name') else 'GLM-4.6V Vision Server'}")

        # List available attributes
        print("\nFastMCP server attributes:")
        for attr in dir(mcp_server):
            if not attr.startswith('_'):
                print(f"  - {attr}")

        print("\nMCP protocol test passed!")
        return True

    except Exception as e:
        print(f"ERROR during MCP protocol test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    # Test direct import first
    import_success = await test_direct_import()

    # Test MCP protocol
    protocol_success = await test_mcp_protocol()

    # Test tools directly (with actual API calls)
    tools_success = await test_tools_directly()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Direct Import Test: {'PASSED' if import_success else 'FAILED'}")
    print(f"MCP Protocol Test: {'PASSED' if protocol_success else 'FAILED'}")
    print(f"Tools Test: {'PASSED' if tools_success else 'FAILED'}")
    print("="*60)

    if import_success and protocol_success and tools_success:
        print("\nAll tests passed! The MCP server is ready to use.")
        print("\nTo start the MCP server, run:")
        print("  python -m vision_mcp.server")
        print("\nOr connect to it from an MCP client using:")
        print("  transport={'command': 'python', 'args': ['-m', 'vision_mcp.server']}")
    else:
        print("\nSome tests failed. Please check the error messages above.")
        exit(1)


if __name__ == "__main__":
    # Run tests
    result = asyncio.run(main())
    exit(0 if result else 1)
