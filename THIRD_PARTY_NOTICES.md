# Third-party notices

## HoudiniMCP

`houdini-cli setup` can download HoudiniMCP from <https://github.com/capoomgit/houdini-mcp.git> at commit `de4fd93acc207fc57c02b330d421461f5963a945`. Setup also creates a derived runtime copy of `houdini_mcp_server.py`; that copy may contain a compatibility change for the LangChain output-parser import.

MIT License

Copyright (c) 2025 Capoom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Python runtime packages

Setup installs the following pinned Python packages and their transitive dependencies into the CLI-owned runtime: `mcp[cli] 1.4.1`, `requests 2.32.5`, `python-dotenv 1.0.1`, and `langchain-classic 1.0.8`. Their distributions include their own license metadata and license files in the isolated environment.

SideFX Houdini, Python, Qt, and PySide6 are supplied by the user's Houdini installation and are not redistributed by this project.
