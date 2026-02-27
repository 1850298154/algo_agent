# GLM-4.6V Vision MCP Server

A Model Context Protocol (MCP) server that provides image analysis capabilities using Zhipu AI's GLM-4.6V vision model.

## Features

- **Image Analysis**: Analyze images with custom prompts
- **Text Extraction (OCR)**: Extract text content from images
- **Object Detection**: Identify objects and UI elements in images
- **Screenshot Analysis**: Specialized tools for webpage screenshots

## Installation

1. Ensure you have Python 3.10+ installed
2. Install dependencies:

```bash
pip install -e .
```

Or manually:

```bash
pip install openai python-dotenv fastmcp pillow mcp
```

## Configuration

Set your Zhipu AI API key in your `.env` file:

```env
ZHIPU_API_KEY=your_api_key_here
```

Get your API key from: https://open.bigmodel.cn/

## Available Tools

### 1. `analyze_image`

General image analysis with custom prompts.

**Parameters:**
- `image_path` (str): Absolute path to the image file
- `prompt` (str): Question or instruction for analyzing the image
- `temperature` (float, optional): Temperature for the model (0-1), default 0.7

**Example:**
```python
{
  "image_path": "/path/to/screenshot.png",
  "prompt": "What information is shown in this webpage?",
  "temperature": 0.7
}
```

### 2. `extract_text_from_image`

Extract all text content from an image (OCR).

**Parameters:**
- `image_path` (str): Absolute path to the image file

**Example:**
```python
{
  "image_path": "/path/to/document.png"
}
```

### 3. `detect_objects_in_image`

Detect and list objects visible in an image.

**Parameters:**
- `image_path` (str): Absolute path to the image file

**Example:**
```python
{
  "image_path": "/path/to/screenshot.png"
}
```

## Usage

### Running the Server

Start the MCP server:

```bash
python -m vision_mcp.server
```

Or using the installed script:

```bash
vision-mcp
```

### Testing

Run the test script:

```bash
python vision_mcp/test_server.py
```

This will:
1. Create a test screenshot image
2. Test all available tools
3. Verify MCP server connectivity

## Connecting from MCP Client

### Using FastMCP Client

```python
from fastmcp import Client

# Connect to the server
client = Client(
    command="python",
    args=["-m", "vision_mcp.server"]
)

async with client:
    # List available tools
    tools = await client.list_tools()

    # Call a tool
    result = await client.call_tool(
        "analyze_image",
        arguments={
            "image_path": "/path/to/image.png",
            "prompt": "Describe what you see"
        }
    )
    print(result.content[0].text)
```

### Using with Claude Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "glm-4.6v-vision": {
      "command": "python",
      "args": ["-m", "vision_mcp.server"]
    }
  }
}
```

## Supported Image Formats

- PNG (.png)
- JPEG/JPG (.jpg, .jpeg)
- WebP (.webp)

## Project Structure

```
vision_mcp/
├── __init__.py          # Package initialization
├── server.py            # MCP server implementation
├── test_server.py       # Test script
├── test_images/        # Test images (created by test script)
├── pyproject.toml      # Project configuration
└── README.md          # This file
```

## API Reference

### Model

- **Model**: `glm-4.6v`
- **Provider**: Zhipu AI (智谱AI)
- **API Base**: `https://open.bigmodel.cn/api/paas/v4/`

### Capabilities

- Image understanding and analysis
- Text extraction (OCR)
- Object detection
- Visual question answering
- UI element identification

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Support

For issues and questions, please open an issue in the repository.
