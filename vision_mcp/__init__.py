"""
GLM-4.6V Vision MCP Server

A Model Context Protocol (MCP) server that provides image analysis capabilities
using Zhipu AI's GLM-4.6V vision model.
"""

__version__ = "0.1.0"
__author__ = "algo_agent"

from .server import main

__all__ = ["main"]
