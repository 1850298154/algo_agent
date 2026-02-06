# MCP Wiki Server

This is the MCP (Model Context Protocol) version of the original HTTP-based wiki operations script.

## Files

- `devin_mcp_server.py` - The MCP server implementation
- `mcp_client_example.py` - Example client showing how to use the server
- `requirements_mcp.txt` - Required dependencies
- `devin_http_save_all_sample.py` - Original HTTP-based script (for reference)

## Installation

1. Install dependencies:
```bash
pip install -r requirements_mcp.txt
```

## Usage

### As MCP Server

The server can be used with any MCP-compatible client (like Claude Desktop, Cursor, etc.).

### Running the Example Client

```bash
python mcp_client_example.py
```

## Available Tools

1. **read_wiki_structure** - Read repository structure
2. **read_wiki_contents** - Read repository contents  
3. **ask_question** - Ask questions about the repository
4. **save_all_wiki_data** - Execute all three operations and save to files

## Key Differences from HTTP Version

1. **Protocol**: Uses MCP instead of direct HTTP calls
2. **Structure**: Implements proper MCP server with tool definitions
3. **Async**: Uses async/await for better performance
4. **Standardized**: Follows MCP specifications for better compatibility
5. **Combined Tool**: Added `save_all_wiki_data` tool that replicates the original script's behavior

## MCP vs Original HTTP

| Aspect | Original HTTP | MCP Version |
|--------|---------------|-------------|
| Communication | Direct HTTP requests | MCP protocol |
| Structure | Simple script | Server with tool definitions |
| Usage | Standalone execution | Client-server architecture |
| Integration | Limited | Compatible with MCP ecosystem |
| Error Handling | Basic | Structured error responses |
