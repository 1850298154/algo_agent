"""
GLM-4.6V Vision MCP Server

Provides image analysis capabilities using Zhipu AI's GLM-4.6V vision model.
"""

import base64
import os
import asyncio
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Create MCP Server
mcp = FastMCP("GLM-4.6V Vision Server")

# Initialize Zhipu AI Client
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    raise ValueError("ZHIPU_API_KEY environment variable is not set")

client = OpenAI(
    api_key=ZHIPU_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

# Model configuration
GLM_4_6V_MODEL = "glm-4.6v"


def encode_image(image_path: str) -> str:
    """Encode image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class ImageAnalysisRequest(BaseModel):
    """Request model for image analysis."""
    image_path: str = Field(..., description="Absolute path to the image file to analyze")
    prompt: str = Field(..., description="Question or instruction for analyzing the image")
    temperature: Optional[float] = Field(0.7, description="Temperature for the model (0-1), default 0.7")


class ImageAnalysisResult(BaseModel):
    """Result model for image analysis."""
    success: bool
    analysis: str
    image_path: str
    model_used: str


@mcp.tool()
async def analyze_image(
    image_path: str,
    prompt: str,
    temperature: float = 0.7
) -> str:
    """
    Analyze an image using GLM-4.6V vision model.

    This tool analyzes images and provides detailed descriptions, answers questions,
    or performs visual tasks using the GLM-4.6V multimodal model.

    Args:
        image_path: Absolute path to the image file (PNG, JPG, JPEG supported)
        prompt: Question or instruction for analyzing the image
        temperature: Temperature for the model (0-1), default 0.7

    Returns:
        Analysis result from the vision model

    Example:
        analyze_image(
            image_path="/path/to/screenshot.png",
            prompt="What information is shown in this webpage screenshot?"
        )
    """
    try:
        # Validate image file exists
        img_path = Path(image_path)
        if not img_path.exists():
            return f"Error: Image file not found at {image_path}"

        # Check file extension
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        if img_path.suffix.lower() not in allowed_extensions:
            return f"Error: Unsupported image format. Supported formats: {', '.join(allowed_extensions)}"

        # Encode image to base64
        image_base64 = encode_image(str(img_path))

        # Call GLM-4.6V API
        response = client.chat.completions.create(
            model=GLM_4_6V_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=temperature
        )

        # Extract and return analysis
        analysis = response.choices[0].message.content

        result = ImageAnalysisResult(
            success=True,
            analysis=analysis,
            image_path=image_path,
            model_used=GLM_4_6V_MODEL
        )

        return (
            f"Image Analysis Result:\n"
            f"====================\n"
            f"Image: {image_path}\n"
            f"Model: {GLM_4_6V_MODEL}\n"
            f"Analysis:\n{analysis}\n"
        )

    except FileNotFoundError:
        return f"Error: Image file not found at {image_path}"
    except Exception as e:
        return f"Error analyzing image: {str(e)}"


@mcp.tool()
async def extract_text_from_image(image_path: str) -> str:
    """
    Extract all text content from an image using GLM-4.6V.

    This tool uses OCR capabilities to extract text from screenshots,
    documents, or any image containing text.

    Args:
        image_path: Absolute path to the image file

    Returns:
        Extracted text content from the image

    Example:
        extract_text_from_image(image_path="/path/to/document.png")
    """
    try:
        img_path = Path(image_path)
        if not img_path.exists():
            return f"Error: Image file not found at {image_path}"

        image_base64 = encode_image(str(img_path))

        response = client.chat.completions.create(
            model=GLM_4_6V_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请提取这张图片中的所有文字内容，按原文格式输出，不要添加任何额外的解释或说明。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.3  # Lower temperature for more accurate text extraction
        )

        text_content = response.choices[0].message.content

        return (
            f"Extracted Text:\n"
            f"================\n"
            f"Image: {image_path}\n"
            f"Content:\n{text_content}\n"
        )

    except Exception as e:
        return f"Error extracting text: {str(e)}"


@mcp.tool()
async def detect_objects_in_image(image_path: str) -> str:
    """
    Detect and list objects visible in an image.

    This tool identifies and lists objects, UI elements, or items visible in the image.

    Args:
        image_path: Absolute path to the image file

    Returns:
        List of detected objects/elements in the image

    Example:
        detect_objects_in_image(image_path="/path/to/screenshot.png")
    """
    try:
        img_path = Path(image_path)
        if not img_path.exists():
            return f"Error: Image file not found at {image_path}"

        image_base64 = encode_image(str(img_path))

        response = client.chat.completions.create(
            model=GLM_4_6V_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请详细描述这张图片中可以看到的所有元素、物体、界面组件或内容。请以结构化的列表形式输出，包括每个元素的位置、类型和简要描述。"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        return (
            f"Detected Objects/Elements:\n"
            f"=========================\n"
            f"Image: {image_path}\n"
            f"{content}\n"
        )

    except Exception as e:
        return f"Error detecting objects: {str(e)}"


@mcp.resource("vision://info")
def get_model_info() -> str:
    """
    Get information about the GLM-4.6V vision model.

    Returns model details including version and capabilities.
    """
    return f"""
GLM-4.6V Vision Model Information
================================

Model Name: {GLM_4_6V_MODEL}
Provider: Zhipu AI (智谱AI)
API Base: https://open.bigmodel.cn/api/paas/v4/

Capabilities:
- Image understanding and analysis
- Text extraction (OCR)
- Object detection
- Visual question answering
- UI element identification

Supported Image Formats:
- PNG
- JPG/JPEG
- WebP

Tools Available:
1. analyze_image - General image analysis with custom prompts
2. extract_text_from_image - Extract text content from images
3. detect_objects_in_image - Detect objects/elements in images
"""


@mcp.prompt()
def analyze_screenshot(image_path: str, task_description: str) -> str:
    """
    Generate a prompt template for analyzing screenshots.

    Args:
        image_path: Path to the screenshot image
        task_description: Description of what to analyze

    Returns:
        Formatted prompt for the AI to analyze the screenshot
    """
    return f"""Please analyze the screenshot at {image_path}.

Task: {task_description}

Use the analyze_image tool to perform this analysis.
"""


def main():
    """Main entry point for running the MCP server."""
    import mcp.server.stdio
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
