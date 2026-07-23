## MCP (Model Context Protocol) Cheat Sheet 

> **Project:** Expense Tracker MCP Server

> **Remote MCP Endpoint:** https://xptracker-server.fastmcp.app/mcp

---

####  What is MCP?
**MCP (Model Context Protocol)** is an open protocol that allows AI models to securely communicate with external tools, APIs, databases, files, and services.

Think of MCP as a **bridge between an AI model and your Python code**.
```
User
   │
   ▼
AI Model
   │
   ▼
MCP Client
   │
   ▼
MCP Server
   │
   ▼
Python Function / Database / API
```

---

#### Why was MCP created?

Without MCP:
* AI cannot access databases.
* AI cannot execute your Python functions.
* AI cannot use external APIs.
* AI cannot interact with your applications.

With MCP:
* AI can call tools.
* AI can query databases.
* AI can read and write files.
* AI can access APIs.
* AI can automate workflows.

---

### Core Components

#### 1. MCP Client
The client connects the AI model to one or more MCP servers.

Examples:
* Claude Desktop
* Cursor
* VS Code
* LangGraph
* Custom Python applications

```
AI
 │
 ▼
MCP Client
```

---

#### 2. MCP Server
The server exposes tools and resources.

Example:
```python
@mcp.tool()
def add(a: int, b: int):
    return a + b
```

The AI can now call the `add` tool automatically.

---

#### 3. Tool
A tool is simply a Python function exposed through MCP.

Example:
```python
@mcp.tool()
async def add_expense(...):
```

Think of a tool as an API endpoint that the AI can call.

---

#### 4. Resource
Resources expose read-only data.

Example:
```python
@mcp.resource("expense:///categories")
```

Resources are commonly used for:
* JSON
* Configuration
* Documentation
* Static data

---

### MCP Architecture

```
            User
              │
              ▼
         AI Assistant
              │
              ▼
         MCP Client
              │
      ┌───────┴────────┐
      ▼                ▼
 Local Server     Remote Server
 (stdio)            (HTTP)
      │                 │
      ▼                 ▼
Python Tools      Python Tools
      │                 │
      ▼                 ▼
 Database/API     Database/API
```

---

### Local vs Remote MCP

#### Local MCP (stdio)
Runs on your computer.
```
Claude Desktop

↓

stdio

↓

Your MCP Server
```

Pros:
* Fast
* Secure
* Great for development

Cons:
* Only available while your computer is running

---

#### Remote MCP (HTTP)
Runs in the cloud.
```
Internet

↓

https://your-server.fastmcp.app/mcp
```

Pros:
* Accessible from anywhere
* Runs 24×7
* Easy to share

---

### Transport Types

#### stdio
Communication happens through standard input/output.

Best for:
* Claude Desktop
* Cursor
* VS Code

Example:
```python
mcp.run()
```

---

#### HTTP / Streamable HTTP
Communication happens over the internet.

Best for:
* Cloud deployment
* Production
* APIs

Example:

```
https://xptracker-server.fastmcp.app/mcp
```
---

### Expense Tracker MCP Example

Tools:
```
add_expense()

list_expenses()

summarize()
```

Resources:
```
expense:///categories
```

Database:

```
SQLite
```

---

### Deployment Flow

```
Laptop

↓

GitHub

↓

FastMCP Cloud

↓

Install Dependencies

↓

Run Server

↓

Public MCP URL
```

Example endpoint:

```
https://xptracker-server.fastmcp.app/mcp
```

---

### Client Configuration

Example:
```python
SERVERS = {
    "expense": {
        "transport": "streamable_http",
        "url": "https://xptracker-server.fastmcp.app/mcp"
    }
}
```

---

#### Tool Execution Flow
Suppose the user says:

```
Add ₹500 Food expense
```

Flow:

```
User

↓

AI

↓

MCP Client

↓

add_expense()

↓

SQLite

↓

Result

↓

AI Response
```

---

### Interview Questions

#### What is MCP?
A protocol that enables AI models to communicate with external tools, services, databases, and applications.

---

#### Difference between MCP Client and MCP Server?

Client:
* Receives AI requests
* Chooses tools
* Sends requests to servers

Server:
* Hosts tools
* Executes Python code
* Returns results

---

#### What is a Tool?
A Python function exposed using:

```python
@mcp.tool()
```

---

#### What is a Resource?

Read-only content exposed using:

```python
@mcp.resource()
```

---

#### Difference between Tool and Resource?

Tool:
* Performs actions
* Accepts parameters
* Returns results

Resource:
* Read-only
* Static information
* No execution

---

#### What is stdio transport?

Communication through standard input/output.
Mostly used for desktop clients.

---

#### What is HTTP transport?

Communication over HTTP.
Used for cloud-hosted MCP servers.

---

#### Why deploy MCP?

To make your tools available:
* 24×7
* Anywhere
* To multiple AI clients

---

#### Why FastMCP?

* Simple API
* Automatic tool discovery
* Easy deployment
* Async support
* HTTP and stdio transports

---

### Best Practices

* Keep tools focused on one responsibility.
* Validate user input.
* Write meaningful docstrings.
* Use async for I/O operations.
* Store secrets in environment variables.
* Handle errors gracefully.
* Return structured JSON responses.
* Log important events.

---

#### Common Mistakes

❌ Forgetting `@mcp.tool()`

❌ Missing async for database operations

❌ Blocking I/O inside async functions

❌ Hardcoding secrets

❌ No error handling

❌ Returning inconsistent response formats

---

#### Real-World MCP Use Cases

* Expense Tracker
* Weather Assistant
* Calendar Assistant
* GitHub Assistant
* SQL Database Assistant
* PDF Search (RAG)
* Customer Support Bot
* CRM Integration
* DevOps Automation
* Kubernetes Operations

---

### Interview Summary (Remember These)

✅ MCP = Bridge between AI and external systems

✅ Client discovers and calls tools

✅ Server executes business logic

✅ Tool = Executable function

✅ Resource = Read-only data

✅ stdio = Local desktop communication

✅ HTTP = Remote cloud communication

✅ FastMCP simplifies building MCP servers

✅ Deploy to cloud to expose a public `/mcp` endpoint

---

### Interview Answer

> Model Context Protocol (MCP) is an open protocol that standardizes how AI models interact with external tools, resources, and services. An MCP Client discovers available tools from an MCP Server and invokes them when needed. The server contains business logic written in languages like Python and can access databases, APIs, or files. MCP supports local communication through `stdio` and remote communication over HTTP, making it easy to integrate AI assistants with real-world applications.

---
