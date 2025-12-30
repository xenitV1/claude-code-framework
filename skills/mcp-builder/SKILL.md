---
name: mcp-builder
description: MCP (Model Context Protocol) server creation for integrating external services with AI.
---

# MCP Builder

> Source: travisvn/awesome-claude-skills

## Overview
Guide for building MCP servers to integrate external APIs and services with Claude.

## MCP Server Structure

```
my-mcp-server/
├── src/
│   └── index.ts
├── package.json
└── tsconfig.json
```

## Basic Server

```typescript
// src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server(
  { name: 'my-mcp-server', version: '1.0.0' },
  { capabilities: { tools: {}, resources: {}, prompts: {} } }
);

// Define a tool
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'get_weather',
      description: 'Get weather for a location',
      inputSchema: {
        type: 'object',
        properties: {
          location: { type: 'string', description: 'City name' }
        },
        required: ['location']
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  switch (request.params.name) {
    case 'get_weather':
      const location = request.params.arguments.location;
      // Call weather API
      return { content: [{ type: 'text', text: `Weather in ${location}: Sunny` }] };
    default:
      throw new Error('Unknown tool');
  }
});

// Start server
const transport = new StdioServerTransport();
server.connect(transport);
```

## Package.json

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0"
  }
}
```

## Configuration

Add to Claude's MCP config:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["./path/to/dist/index.js"]
    }
  }
}
```

## Agentic & Multimodal Patterns (2025)

### Handling Multimodal Data
```typescript
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'analyze_image') {
    const { base64, mimeType } = request.params.arguments;
    // Process image context...
  }
});
```

### Sampling (Agent-to-LLM Request)
```typescript
// Server requesting LLM to complete a task
const result = await server.createMessage({
  messages: [{ role: 'user', content: [{ type: 'text', text: 'summarize this...' }] }]
});
```

## Best Practices
1. **Clear tool names** - Descriptive, action-oriented.
2. **Structured Output** - Use JSON Schema for predictable tool results.
3. **MCP Registry** - Verify compatibility with official MCP Registry standards.
