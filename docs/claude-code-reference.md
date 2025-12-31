# Subagents

> Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

Custom subagents in Claude Code are specialized AI assistants that can be invoked to handle specific types of tasks. They enable more efficient problem-solving by providing task-specific configurations with customized system prompts, tools and a separate context window.

## What are subagents?

Subagents are pre-configured AI personalities that Claude Code can delegate tasks to. Each subagent:

* Has a specific purpose and expertise area
* Uses its own context window separate from the main conversation
* Can be configured with specific tools it's allowed to use
* Includes a custom system prompt that guides its behavior

When Claude Code encounters a task that matches a subagent's expertise, it can delegate that task to the specialized subagent, which works independently and returns results.

## Key benefits

<CardGroup cols={2}>
  <Card title="Context preservation" icon="layer-group">
    Each subagent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives.
  </Card>

  <Card title="Specialized expertise" icon="brain">
    Subagents can be fine-tuned with detailed instructions for specific domains, leading to higher success rates on designated tasks.
  </Card>

  <Card title="Reusability" icon="rotate">
    Once created, you can use subagents across different projects and share them with your team for consistent workflows.
  </Card>

  <Card title="Flexible permissions" icon="shield-check">
    Each subagent can have different tool access levels, allowing you to limit powerful tools to specific subagent types.
  </Card>
</CardGroup>

## Quick start

To create your first subagent:

<Steps>
  <Step title="Open the subagents interface">
    Run the following command:

    ```
    /agents
    ```
  </Step>

  <Step title="Select 'Create New Agent'">
    Choose whether to create a project-level or user-level subagent
  </Step>

  <Step title="Define the subagent">
    * **Recommended**: generate with Claude first, then customize to make it yours
    * Describe your subagent in detail, including when Claude should use it
    * Select the tools you want to grant access to, or leave this blank to inherit all tools
    * The interface shows all available tools
    * If you're generating with Claude, you can also edit the system prompt in your own editor by pressing `e`
  </Step>

  <Step title="Save and use">
    Your subagent is now available. Claude uses it automatically when appropriate, or you can invoke it explicitly:

    ```
    > Use the code-reviewer subagent to check my recent changes
    ```
  </Step>
</Steps>

## Subagent configuration

### File locations

Subagents are stored as Markdown files with YAML frontmatter in two possible locations:

| Type                  | Location            | Scope                         | Priority |
| :-------------------- | :------------------ | :---------------------------- | :------- |
| **Project subagents** | `.claude/agents/`   | Available in current project  | Highest  |
| **User subagents**    | `~/.claude/agents/` | Available across all projects | Lower    |

When subagent names conflict, project-level subagents take precedence over user-level subagents.

### Plugin agents

[Plugins](/en/plugins) can provide custom subagents that integrate seamlessly with Claude Code. Plugin agents work identically to user-defined agents and appear in the `/agents` interface.

**Plugin agent locations**: plugins include agents in their `agents/` directory (or custom paths specified in the plugin manifest).

**Using plugin agents**:

* Plugin agents appear in `/agents` alongside your custom agents
* Can be invoked explicitly: "Use the code-reviewer agent from the security-plugin"
* Can be invoked automatically by Claude when appropriate
* Can be managed (viewed, inspected) through `/agents` interface

See the [plugin components reference](/en/plugins-reference#agents) for details on creating plugin agents.

### CLI-based configuration

You can also define subagents dynamically using the `--agents` CLI flag, which accepts a JSON object:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**Priority**: CLI-defined subagents have lower priority than project-level subagents but higher priority than user-level subagents.

**Use case**: This approach is useful for:

* Quick testing of subagent configurations
* Session-specific subagents that don't need to be saved
* Automation scripts that need custom subagents
* Sharing subagent definitions in documentation or scripts

For detailed information about the JSON format and all available options, see the [CLI reference documentation](/en/cli-reference#agents-flag-format).

### File format

Each subagent is defined in a Markdown file with this structure:

```markdown  theme={null}
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
permissionMode: default  # Optional - permission mode for the subagent
skills: skill1, skill2  # Optional - skills to auto-load
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

#### Configuration fields

| Field            | Required | Description                                                                                                                                                                                                     |
| :--------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`           | Yes      | Unique identifier using lowercase letters and hyphens                                                                                                                                                           |
| `description`    | Yes      | Natural language description of the subagent's purpose                                                                                                                                                          |
| `tools`          | No       | Comma-separated list of specific tools. If omitted, inherits all tools from the main thread                                                                                                                     |
| `model`          | No       | Model to use for this subagent. Can be a model alias (`sonnet`, `opus`, `haiku`) or `'inherit'` to use the main conversation's model. If omitted, defaults to the [configured subagent model](/en/model-config) |
| `permissionMode` | No       | Permission mode for the subagent. Valid values: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`. Controls how the subagent handles permission requests                                          |
| `skills`         | No       | Comma-separated list of skill names to auto-load when the subagent starts. Subagents do not inherit Skills from the parent conversation. If omitted, no Skills are preloaded.                                   |

### Model selection

The `model` field allows you to control which [AI model](/en/model-config) the subagent uses:

* **Model alias**: Use one of the available aliases: `sonnet`, `opus`, or `haiku`
* **`'inherit'`**: Use the same model as the main conversation (useful for consistency)
* **Omitted**: If not specified, uses the default model configured for subagents (`sonnet`)

<Note>
  Using `'inherit'` is particularly useful when you want your subagents to adapt to the model choice of the main conversation, ensuring consistent capabilities and response style throughout your session.
</Note>

### Available tools

Subagents can be granted access to any of Claude Code's internal tools. See the [tools documentation](/en/settings#tools-available-to-claude) for a complete list of available tools.

<Tip>
  **Recommended:** Use the `/agents` command to modify tool access - it provides an interactive interface that lists all available tools, including any connected MCP server tools, making it easier to select the ones you need.
</Tip>

You have two options for configuring tools:

* **Omit the `tools` field** to inherit all tools from the main thread (default), including MCP tools
* **Specify individual tools** as a comma-separated list for more granular control (can be edited manually or via `/agents`)

**MCP Tools**: Subagents can access MCP tools from configured MCP servers. When the `tools` field is omitted, subagents inherit all MCP tools available to the main thread.

## Managing subagents

### Using the /agents command (Recommended)

The `/agents` command provides a comprehensive interface for subagent management:

```
/agents
```

This opens an interactive menu where you can:

* View all available subagents (built-in, user, and project)
* Create new subagents with guided setup
* Edit existing custom subagents, including their tool access
* Delete custom subagents
* See which subagents are active when duplicates exist
* **Manage tool permissions** with a complete list of available tools

### Direct file management

You can also manage subagents by working directly with their files:

```bash  theme={null}
# Create a project subagent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# Create a user subagent
mkdir -p ~/.claude/agents
# ... create subagent file
```

<Note>
  Subagents created by manually adding files will be loaded the next time you start a Claude Code session. To create and use a subagent immediately without restarting, use the `/agents` command instead.
</Note>

## Using subagents effectively

### Automatic delegation

Claude Code proactively delegates tasks based on:

* The task description in your request
* The `description` field in subagent configurations
* Current context and available tools

<Tip>
  To encourage more proactive subagent use, include phrases like "use PROACTIVELY" or "MUST BE USED" in your `description` field.
</Tip>

### Explicit invocation

Request a specific subagent by mentioning it in your command:

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

## Built-in subagents

Claude Code includes built-in subagents that are available out of the box:

### General-purpose subagent

The general-purpose subagent is a capable agent for complex, multi-step tasks that require both exploration and action. Unlike the Explore subagent, it can modify files and execute a wider range of operations.

**Key characteristics:**

* **Model**: Uses Sonnet for more capable reasoning
* **Tools**: Has access to all tools
* **Mode**: Can read and write files, execute commands, make changes
* **Purpose**: Complex research tasks, multi-step operations, code modifications

**When Claude uses it:**

Claude delegates to the general-purpose subagent when:

* The task requires both exploration and modification
* Complex reasoning is needed to interpret search results
* Multiple strategies may be needed if initial searches fail
* The task has multiple steps that depend on each other

**Example scenario:**

```
User: Find all the places where we handle authentication and update them to use the new token format

Claude: [Invokes general-purpose subagent]
[Agent searches for auth-related code across codebase]
[Agent reads and analyzes multiple files]
[Agent makes necessary edits]
[Returns detailed writeup of changes made]
```

### Plan subagent

The Plan subagent is a specialized built-in agent designed for use during plan mode. When Claude is operating in plan mode (non-execution mode), it uses the Plan subagent to conduct research and gather information about your codebase before presenting a plan.

**Key characteristics:**

* **Model**: Uses Sonnet for more capable analysis
* **Tools**: Has access to Read, Glob, Grep, and Bash tools for codebase exploration
* **Purpose**: Searches files, analyzes code structure, and gathers context
* **Automatic invocation**: Claude automatically uses this agent when in plan mode and needs to research the codebase

**How it works:**
When you're in plan mode and Claude needs to understand your codebase to create a plan, it delegates research tasks to the Plan subagent. This prevents infinite nesting of agents (subagents cannot spawn other subagents) while still allowing Claude to gather the necessary context.

**Example scenario:**

```
User: [In plan mode] Help me refactor the authentication module

Claude: Let me research your authentication implementation first...
[Internally invokes Plan subagent to explore auth-related files]
[Plan subagent searches codebase and returns findings]
Claude: Based on my research, here's my proposed plan...
```

<Tip>
  The Plan subagent is only used in plan mode. In normal execution mode, Claude uses the general-purpose agent or other custom subagents you've created.
</Tip>

### Explore subagent

The Explore subagent is a fast, lightweight agent optimized for searching and analyzing codebases. It operates in strict read-only mode and is designed for rapid file discovery and code exploration.

**Key characteristics:**

* **Model**: Uses Haiku for fast, low-latency searches
* **Mode**: Strictly read-only - cannot create, modify, or delete files
* **Tools available**:
  * Glob - File pattern matching
  * Grep - Content searching with regular expressions
  * Read - Reading file contents
  * Bash - Read-only commands only (ls, git status, git log, git diff, find, cat, head, tail)

**When Claude uses it:**

Claude will delegate to the Explore subagent when it needs to search or understand a codebase but doesn't need to make changes. This is more efficient than the main agent running multiple search commands directly, as content found during the exploration process doesn't bloat the main conversation.

**Thoroughness levels:**

When invoking the Explore subagent, Claude specifies a thoroughness level:

* **Quick** - Fast searches with minimal exploration. Good for targeted lookups.
* **Medium** - Moderate exploration. Balances speed and thoroughness.
* **Very thorough** - Comprehensive analysis across multiple locations and naming conventions. Used when the target might be in unexpected places.

**Example scenarios:**

```
User: Where are errors from the client handled?

Claude: [Invokes Explore subagent with "medium" thoroughness]
[Explore uses Grep to search for error handling patterns]
[Explore uses Read to examine promising files]
[Returns findings with absolute file paths]
Claude: Client errors are handled in src/services/process.ts:712...
```

```
User: What's the codebase structure?

Claude: [Invokes Explore subagent with "quick" thoroughness]
[Explore uses Glob and ls to map directory structure]
[Returns overview of key directories and their purposes]
```

## Example subagents

### Code reviewer

```markdown  theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

```markdown  theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data scientist

```markdown  theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

## Best practices

* **Start with Claude-generated agents**: We highly recommend generating your initial subagent with Claude and then iterating on it to make it personally yours. This approach gives you the best results - a solid foundation that you can customize to your specific needs.

* **Design focused subagents**: Create subagents with single, clear responsibilities rather than trying to make one subagent do everything. This improves performance and makes subagents more predictable.

* **Write detailed prompts**: Include specific instructions, examples, and constraints in your system prompts. The more guidance you provide, the better the subagent will perform.

* **Limit tool access**: Only grant tools that are necessary for the subagent's purpose. This improves security and helps the subagent focus on relevant actions.

* **Version control**: Check project subagents into version control so your team can benefit from and improve them collaboratively.

## Advanced usage

### Chaining subagents

For complex workflows, you can chain multiple subagents:

```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Dynamic subagent selection

Claude Code intelligently selects subagents based on context. Make your `description` fields specific and action-oriented for best results.

### Resumable subagents

Subagents can be resumed to continue previous conversations, which is particularly useful for long-running research or analysis tasks that need to be continued across multiple invocations.

**How it works:**

* Each subagent execution is assigned a unique `agentId`
* The agent's conversation is stored in a separate transcript file: `agent-{agentId}.jsonl`
* You can resume a previous agent by providing its `agentId` via the `resume` parameter
* When resumed, the agent continues with full context from its previous conversation

**Example workflow:**

Initial invocation:

```
> Use the code-analyzer agent to start reviewing the authentication module

[Agent completes initial analysis and returns agentId: "abc123"]
```

Resume the agent:

```
> Resume agent abc123 and now analyze the authorization logic as well

[Agent continues with full context from previous conversation]
```

**Use cases:**

* **Long-running research**: Break down large codebase analysis into multiple sessions
* **Iterative refinement**: Continue refining a subagent's work without losing context
* **Multi-step workflows**: Have a subagent work on related tasks sequentially while maintaining context

**Technical details:**

* Agent transcripts are stored in your project directory
* Recording is disabled during resume to avoid duplicating messages
* Both synchronous and asynchronous agents can be resumed
* The `resume` parameter accepts the agent ID from a previous execution

**Programmatic usage:**

If you're using the Agent SDK or interacting with the AgentTool directly, you can pass the `resume` parameter:

```typescript  theme={null}
{
  "description": "Continue analysis",
  "prompt": "Now examine the error handling patterns",
  "subagent_type": "code-analyzer",
  "resume": "abc123"  // Agent ID from previous execution
}
```

<Tip>
  Keep track of agent IDs for tasks you may want to resume later. Claude Code displays the agent ID when a subagent completes its work.
</Tip>

## Performance considerations

* **Context efficiency**: Agents help preserve main context, enabling longer overall sessions
* **Latency**: Subagents start off with a clean slate each time they are invoked and may add latency as they gather context that they require to do their job effectively.

## Related documentation

* [Plugins](/en/plugins) - Extend Claude Code with custom agents through plugins
* [Slash commands](/en/slash-commands) - Learn about other built-in commands
* [Settings](/en/settings) - Configure Claude Code behavior
* [Hooks](/en/hooks) - Automate workflows with event handlers


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt



# Create plugins

> Create custom plugins to extend Claude Code with slash commands, agents, hooks, Skills, and MCP servers.

Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams. This guide covers creating your own plugins with slash commands, agents, Skills, hooks, and MCP servers.

Looking to install existing plugins? See [Discover and install plugins](/en/discover-plugins). For complete technical specifications, see [Plugins reference](/en/plugins-reference).

## When to use plugins vs standalone configuration

Claude Code supports two ways to add custom slash commands, agents, and hooks:

| Approach                                                    | Slash command names  | Best for                                                                                        |
| :---------------------------------------------------------- | :------------------- | :---------------------------------------------------------------------------------------------- |
| **Standalone** (`.claude/` directory)                       | `/hello`             | Personal workflows, project-specific customizations, quick experiments                          |
| **Plugins** (directories with `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Sharing with teammates, distributing to community, versioned releases, reusable across projects |

**Use standalone configuration when**:

* You're customizing Claude Code for a single project
* The configuration is personal and doesn't need to be shared
* You're experimenting with slash commands or hooks before packaging them
* You want short slash command names like `/hello` or `/review`

**Use plugins when**:

* You want to share functionality with your team or community
* You need the same slash commands/agents across multiple projects
* You want version control and easy updates for your extensions
* You're distributing through a marketplace
* You're okay with namespaced slash commands like `/my-plugin:hello` (namespacing prevents conflicts between plugins)

<Tip>
  Start with standalone configuration in `.claude/` for quick iteration, then [convert to a plugin](#convert-existing-configurations-to-plugins) when you're ready to share.
</Tip>

## Quickstart

This quickstart walks you through creating a plugin with a custom slash command. You'll create a manifest (the configuration file that defines your plugin), add a slash command, and test it locally using the `--plugin-dir` flag.

### Prerequisites

* Claude Code [installed and authenticated](/en/quickstart#step-1-install-claude-code)
* Claude Code version 1.0.33 or later (run `claude --version` to check)

<Note>
  If you don't see the `/plugin` command, update Claude Code to the latest version. See [Troubleshooting](/en/troubleshooting) for upgrade instructions.
</Note>

### Create your first plugin

<Steps>
  <Step title="Create the plugin directory">
    Every plugin lives in its own directory containing a manifest and your custom commands, agents, or hooks. Create one now:

    ```bash  theme={null}
    mkdir my-first-plugin
    ```
  </Step>

  <Step title="Create the plugin manifest">
    The manifest file at `.claude-plugin/plugin.json` defines your plugin's identity: its name, description, and version. Claude Code uses this metadata to display your plugin in the plugin manager.

    Create the `.claude-plugin` directory inside your plugin folder:

    ```bash  theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Then create `my-first-plugin/.claude-plugin/plugin.json` with this content:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
    "name": "my-first-plugin",
    "description": "A greeting plugin to learn the basics",
    "version": "1.0.0",
    "author": {
    "name": "Your Name"
    }
    }
    ```

    | Field         | Purpose                                                                                                                |
    | :------------ | :--------------------------------------------------------------------------------------------------------------------- |
    | `name`        | Unique identifier and slash command namespace. Slash commands are prefixed with this (e.g., `/my-first-plugin:hello`). |
    | `description` | Shown in the plugin manager when browsing or installing plugins.                                                       |
    | `version`     | Track releases using [semantic versioning](/en/plugins-reference#version-management).                                  |
    | `author`      | Optional. Helpful for attribution.                                                                                     |

    For additional fields like `homepage`, `repository`, and `license`, see the [full manifest schema](/en/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Add a slash command">
    Slash commands are Markdown files in the `commands/` directory. The filename becomes the slash command name, prefixed with the plugin's namespace (`hello.md` in a plugin named `my-first-plugin` creates `/my-first-plugin:hello`). The Markdown content tells Claude how to respond when someone runs the slash command.

    Create a `commands` directory in your plugin folder:

    ```bash  theme={null}
    mkdir my-first-plugin/commands
    ```

    Then create `my-first-plugin/commands/hello.md` with this content:

    ```markdown my-first-plugin/commands/hello.md theme={null}
    ---
    description: Greet the user with a friendly message
    ---

    # Hello Command

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Test your plugin">
    Run Claude Code with the `--plugin-dir` flag to load your plugin:

    ```bash  theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Once Claude Code starts, try your new command:

    ```shell  theme={null}
    /my-first-plugin:hello
    ```

    You'll see Claude respond with a greeting. Run `/help` to see your command listed under the plugin namespace.

    <Note>
      **Why namespacing?** Plugin slash commands are always namespaced (like `/greet:hello`) to prevent conflicts when multiple plugins have commands with the same name.

      To change the namespace prefix, update the `name` field in `plugin.json`.
    </Note>
  </Step>

  <Step title="Add slash command arguments">
    Make your slash command dynamic by accepting user input. The `$ARGUMENTS` placeholder captures any text the user provides after the slash command.

    Update your `hello.md` file:

    ```markdown my-first-plugin/commands/hello.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Command

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Restart Claude Code to pick up the changes, then try the command with your name:

    ```shell  theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude will greet you by name. For more argument options like `$1`, `$2` for individual parameters, see [Slash commands](/en/slash-commands).
  </Step>
</Steps>

You've successfully created and tested a plugin with these key components:

* **Plugin manifest** (`.claude-plugin/plugin.json`): describes your plugin's metadata
* **Commands directory** (`commands/`): contains your custom slash commands
* **Command arguments** (`$ARGUMENTS`): captures user input for dynamic behavior

<Tip>
  The `--plugin-dir` flag is useful for development and testing. When you're ready to share your plugin with others, see [Create and distribute a plugin marketplace](/en/plugin-marketplaces).
</Tip>

## Plugin structure overview

You've created a plugin with a slash command, but plugins can include much more: custom agents, Skills, hooks, MCP servers, and LSP servers.

<Warning>
  **Common mistake**: Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root level.
</Warning>

| Directory         | Location    | Purpose                                         |
| :---------------- | :---------- | :---------------------------------------------- |
| `.claude-plugin/` | Plugin root | Contains only `plugin.json` manifest (required) |
| `commands/`       | Plugin root | Slash commands as Markdown files                |
| `agents/`         | Plugin root | Custom agent definitions                        |
| `skills/`         | Plugin root | Agent Skills with `SKILL.md` files              |
| `hooks/`          | Plugin root | Event handlers in `hooks.json`                  |
| `.mcp.json`       | Plugin root | MCP server configurations                       |
| `.lsp.json`       | Plugin root | LSP server configurations for code intelligence |

<Note>
  **Next steps**: Ready to add more features? Jump to [Develop more complex plugins](#develop-more-complex-plugins) to add agents, hooks, MCP servers, and LSP servers. For complete technical specifications of all plugin components, see [Plugins reference](/en/plugins-reference).
</Note>

## Develop more complex plugins

Once you're comfortable with basic plugins, you can create more sophisticated extensions.

### Add Skills to your plugin

Plugins can include [Agent Skills](/en/skills) to extend Claude's capabilities. Skills are model-invoked: Claude automatically uses them based on the task context.

Add a `skills/` directory at your plugin root with Skill folders containing `SKILL.md` files:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Each `SKILL.md` needs frontmatter with `name` and `description` fields, followed by instructions:

```yaml  theme={null}
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

After installing the plugin, restart Claude Code to load the Skills. For complete Skill authoring guidance including progressive disclosure and tool restrictions, see [Agent Skills](/en/skills).

### Add LSP servers to your plugin

<Tip>
  For common languages like TypeScript, Python, and Rust, install the pre-built LSP plugins from the official marketplace. Create custom LSP plugins only when you need support for languages not already covered.
</Tip>

LSP (Language Server Protocol) plugins give Claude real-time code intelligence. If you need to support a language that doesn't have an official LSP plugin, you can create your own by adding an `.lsp.json` file to your plugin:

```json .lsp.json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Users installing your plugin must have the language server binary installed on their machine.

For complete LSP configuration options, see [LSP servers](/en/plugins-reference#lsp-servers).

### Organize complex plugins

For plugins with many components, organize your directory structure by functionality. For complete directory layouts and organization patterns, see [Plugin directory structure](/en/plugins-reference#plugin-directory-structure).

### Test your plugins locally

Use the `--plugin-dir` flag to test plugins during development. This loads your plugin directly without requiring installation.

```bash  theme={null}
claude --plugin-dir ./my-plugin
```

As you make changes to your plugin, restart Claude Code to pick up the updates. Test your plugin components:

* Try your commands with `/command-name`
* Check that agents appear in `/agents`
* Verify hooks work as expected

<Tip>
  You can load multiple plugins at once by specifying the flag multiple times:

  ```bash  theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

### Debug plugin issues

If your plugin isn't working as expected:

1. **Check the structure**: Ensure your directories are at the plugin root, not inside `.claude-plugin/`
2. **Test components individually**: Check each command, agent, and hook separately
3. **Use validation and debugging tools**: See [Debugging and development tools](/en/plugins-reference#debugging-and-development-tools) for CLI commands and troubleshooting techniques

### Share your plugins

When your plugin is ready to share:

1. **Add documentation**: Include a `README.md` with installation and usage instructions
2. **Version your plugin**: Use [semantic versioning](/en/plugins-reference#version-management) in your `plugin.json`
3. **Create or use a marketplace**: Distribute through [plugin marketplaces](/en/plugin-marketplaces) for installation
4. **Test with others**: Have team members test the plugin before wider distribution

Once your plugin is in a marketplace, others can install it using the instructions in [Discover and install plugins](/en/discover-plugins).

<Note>
  For complete technical specifications, debugging techniques, and distribution strategies, see [Plugins reference](/en/plugins-reference).
</Note>

## Convert existing configurations to plugins

If you already have custom commands, Skills, or hooks in your `.claude/` directory, you can convert them into a plugin for easier sharing and distribution.

### Migration steps

<Steps>
  <Step title="Create the plugin structure">
    Create a new plugin directory:

    ```bash  theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Create the manifest file at `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Copy your existing files">
    Copy your existing configurations to the plugin directory:

    ```bash  theme={null}
    # Copy commands
    cp -r .claude/commands my-plugin/

    # Copy agents (if any)
    cp -r .claude/agents my-plugin/

    # Copy skills (if any)
    cp -r .claude/skills my-plugin/
    ```
  </Step>

  <Step title="Migrate hooks">
    If you have hooks in your settings, create a hooks directory:

    ```bash  theme={null}
    mkdir my-plugin/hooks
    ```

    Create `my-plugin/hooks/hooks.json` with your hooks configuration. Copy the `hooks` object from your `.claude/settings.json` or `settings.local.json`—the format is the same:

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "npm run lint:fix $FILE" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Test your migrated plugin">
    Load your plugin to verify everything works:

    ```bash  theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Test each component: run your commands, check agents appear in `/agents`, and verify hooks trigger correctly.
  </Step>
</Steps>

### What changes when migrating

| Standalone (`.claude/`)       | Plugin                           |
| :---------------------------- | :------------------------------- |
| Only available in one project | Can be shared via marketplaces   |
| Files in `.claude/commands/`  | Files in `plugin-name/commands/` |
| Hooks in `settings.json`      | Hooks in `hooks/hooks.json`      |
| Must manually copy to share   | Install with `/plugin install`   |

<Note>
  After migrating, you can remove the original files from `.claude/` to avoid duplicates. The plugin version will take precedence when loaded.
</Note>

## Next steps

Now that you understand Claude Code's plugin system, here are suggested paths for different goals:

### For plugin users

* [Discover and install plugins](/en/discover-plugins): browse marketplaces and install plugins
* [Configure team marketplaces](/en/discover-plugins#configure-team-marketplaces): set up repository-level plugins for your team

### For plugin developers

* [Create and distribute a marketplace](/en/plugin-marketplaces): package and share your plugins
* [Plugins reference](/en/plugins-reference): complete technical specifications
* Dive deeper into specific plugin components:
  * [Slash commands](/en/slash-commands): command development details
  * [Subagents](/en/sub-agents): agent configuration and capabilities
  * [Agent Skills](/en/skills): extend Claude's capabilities
  * [Hooks](/en/hooks): event handling and automation
  * [MCP](/en/mcp): external tool integration


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt

# Discover and install prebuilt plugins through marketplaces

> Find and install plugins from marketplaces to extend Claude Code with new commands, agents, and capabilities.

Plugins extend Claude Code with custom commands, agents, hooks, and MCP servers. Plugin marketplaces are catalogs that help you discover and install these extensions without building them yourself.

Looking to create and distribute your own marketplace? See [Create and distribute a plugin marketplace](/en/plugin-marketplaces).

## How marketplaces work

A marketplace is a catalog of plugins that someone else has created and shared. Using a marketplace is a two-step process:

<Steps>
  <Step title="Add the marketplace">
    This registers the catalog with Claude Code so you can browse what's available. No plugins are installed yet.
  </Step>

  <Step title="Install individual plugins">
    Browse the catalog and install the plugins you want.
  </Step>
</Steps>

Think of it like adding an app store: adding the store gives you access to browse its collection, but you still choose which apps to download individually.

## Official Anthropic marketplace

The official Anthropic marketplace (`claude-plugins-official`) is automatically available when you start Claude Code. Run `/plugin` and go to the **Discover** tab to browse what's available.

To install a plugin from the official marketplace:

```shell  theme={null}
/plugin install plugin-name@claude-plugins-official
```

<Note>
  The official marketplace is maintained by Anthropic. To distribute your own plugins, [create your own marketplace](/en/plugin-marketplaces) and share it with users.
</Note>

The official marketplace includes several categories of plugins:

### Code intelligence

Code intelligence plugins help Claude understand your codebase more deeply. With these plugins installed, Claude can jump to definitions, find references, and see type errors immediately after edits. These plugins use the [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP), the same technology that powers VS Code's code intelligence.

These plugins require the language server binary to be installed on your system. If you already have a language server installed, Claude may prompt you to install the corresponding plugin when you open a project.

| Language   | Plugin              | Binary required              |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

You can also [create your own LSP plugin](/en/plugins-reference#lsp-servers) for other languages.

<Note>
  If you see `Executable not found in $PATH` in the `/plugin` Errors tab after installing a plugin, install the required binary from the table above.
</Note>

### External integrations

These plugins bundle pre-configured [MCP servers](/en/mcp) so you can connect Claude to external services without manual setup:

* **Source control**: `github`, `gitlab`
* **Project management**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design**: `figma`
* **Infrastructure**: `vercel`, `firebase`, `supabase`
* **Communication**: `slack`
* **Monitoring**: `sentry`

### Development workflows

Plugins that add commands and agents for common development tasks:

* **commit-commands**: Git commit workflows including commit, push, and PR creation
* **pr-review-toolkit**: Specialized agents for reviewing pull requests
* **agent-sdk-dev**: Tools for building with the Claude Agent SDK
* **plugin-dev**: Toolkit for creating your own plugins

### Output styles

Customize how Claude responds:

* **explanatory-output-style**: Educational insights about implementation choices
* **learning-output-style**: Interactive learning mode for skill building

## Try it: add the demo marketplace

Anthropic also maintains a [demo plugins marketplace](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) with example plugins that show what's possible with the plugin system. Unlike the official marketplace, you need to add this one manually.

<Steps>
  <Step title="Add the marketplace">
    From within Claude Code, run the `plugin marketplace add` command for the `anthropics/claude-code` marketplace:

    ```shell  theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    This downloads the marketplace catalog and makes its plugins available to you.
  </Step>

  <Step title="Browse available plugins">
    Run `/plugin` to open the plugin manager. This opens a tabbed interface with four tabs you can cycle through using **Tab** (or **Shift+Tab** to go backward):

    * **Discover**: browse available plugins from all your marketplaces
    * **Installed**: view and manage your installed plugins
    * **Marketplaces**: add, remove, or update your added marketplaces
    * **Errors**: view any plugin loading errors

    Go to the **Discover** tab to see plugins from the marketplace you just added.
  </Step>

  <Step title="Install a plugin">
    Select a plugin to view its details, then choose an installation scope:

    * **User scope**: install for yourself across all projects
    * **Project scope**: install for all collaborators on this repository
    * **Local scope**: install for yourself in this repository only

    For example, select **commit-commands** (a plugin that adds git workflow commands) and install it to your user scope.

    You can also install directly from the command line:

    ```shell  theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    See [Configuration scopes](/en/settings#configuration-scopes) to learn more about scopes.
  </Step>

  <Step title="Use your new plugin">
    After installing, the plugin's commands are immediately available. Plugin commands are namespaced by the plugin name, so **commit-commands** provides commands like `/commit-commands:commit`.

    Try it out by making a change to a file and running:

    ```shell  theme={null}
    /commit-commands:commit
    ```

    This stages your changes, generates a commit message, and creates the commit.

    Each plugin works differently. Check the plugin's description in the **Discover** tab or its homepage to learn what commands and capabilities it provides.
  </Step>
</Steps>

The rest of this guide covers all the ways you can add marketplaces, install plugins, and manage your configuration.

## Add marketplaces

Use the `/plugin marketplace add` command to add marketplaces from different sources.

<Tip>
  **Shortcuts**: You can use `/plugin market` instead of `/plugin marketplace`, and `rm` instead of `remove`.
</Tip>

* **GitHub repositories**: `owner/repo` format (for example, `anthropics/claude-code`)
* **Git URLs**: any git repository URL (GitLab, Bitbucket, self-hosted)
* **Local paths**: directories or direct paths to `marketplace.json` files
* **Remote URLs**: direct URLs to hosted `marketplace.json` files

### Add from GitHub

Add a GitHub repository that contains a `.claude-plugin/marketplace.json` file using the `owner/repo` format—where `owner` is the GitHub username or organization and `repo` is the repository name.

For example, `anthropics/claude-code` refers to the `claude-code` repository owned by `anthropics`:

```shell  theme={null}
/plugin marketplace add anthropics/claude-code
```

### Add from other Git hosts

Add any git repository by providing the full URL. This works with any Git host, including GitLab, Bitbucket, and self-hosted servers:

Using HTTPS:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Using SSH:

```shell  theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

To add a specific branch or tag, append `#` followed by the ref:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Add from local paths

Add a local directory that contains a `.claude-plugin/marketplace.json` file:

```shell  theme={null}
/plugin marketplace add ./my-marketplace
```

You can also add a direct path to a `marketplace.json` file:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

Or add a remote `marketplace.json` file via URL:

```shell  theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

## Install plugins

Once you've added marketplaces, you can install plugins directly (installs to user scope by default):

```shell  theme={null}
/plugin install plugin-name@marketplace-name
```

To choose a different [installation scope](/en/settings#configuration-scopes), use the interactive UI: run `/plugin`, go to the **Discover** tab, and press **Enter** on a plugin. You'll see options for:

* **User scope** (default): install for yourself across all projects
* **Project scope**: install for all collaborators on this repository (adds to `.claude/settings.json`)
* **Local scope**: install for yourself in this repository only (not shared with collaborators)

You may also see plugins with **managed** scope—these are installed by enterprise administrators via [managed settings](/en/settings#enterprise-managed-policy-settings) and cannot be modified.

Run `/plugin` and go to the **Installed** tab to see your plugins grouped by scope.

<Warning>
  Make sure you trust a plugin before installing it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they work as intended. Check each plugin's homepage for more information.
</Warning>

## Manage installed plugins

Run `/plugin` and go to the **Installed** tab to view, enable, disable, or uninstall your plugins.

You can also manage plugins with direct commands.

Disable a plugin without uninstalling:

```shell  theme={null}
/plugin disable plugin-name@marketplace-name
```

Re-enable a disabled plugin:

```shell  theme={null}
/plugin enable plugin-name@marketplace-name
```

Completely remove a plugin:

```shell  theme={null}
/plugin uninstall plugin-name@marketplace-name
```

The `--scope` option lets you target a specific scope with CLI commands:

```shell  theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

## Manage marketplaces

You can manage marketplaces through the interactive `/plugin` interface or with CLI commands.

### Use the interactive interface

Run `/plugin` and go to the **Marketplaces** tab to:

* View all your added marketplaces with their sources and status
* Add new marketplaces
* Update marketplace listings to fetch the latest plugins
* Remove marketplaces you no longer need

### Use CLI commands

You can also manage marketplaces with direct commands.

List all configured marketplaces:

```shell  theme={null}
/plugin marketplace list
```

Refresh plugin listings from a marketplace:

```shell  theme={null}
/plugin marketplace update marketplace-name
```

Remove a marketplace:

```shell  theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  Removing a marketplace will uninstall any plugins you installed from it.
</Warning>

### Configure auto-updates

Claude Code can automatically update marketplaces and their installed plugins at startup. When auto-update is enabled for a marketplace, Claude Code refreshes the marketplace data and updates installed plugins to their latest versions. If any plugins were updated, you'll see a notification suggesting you restart Claude Code.

Toggle auto-update for individual marketplaces through the UI:

1. Run `/plugin` to open the plugin manager
2. Select **Marketplaces**
3. Choose a marketplace from the list
4. Select **Enable auto-update** or **Disable auto-update**

Official Anthropic marketplaces have auto-update enabled by default. Third-party and local development marketplaces have auto-update disabled by default.

To disable all automatic updates entirely for both Claude Code and all plugins, set the `DISABLE_AUTOUPDATER` environment variable. See [Auto updates](/en/setup#auto-updates) for details.

## Configure team marketplaces

Team admins can set up automatic marketplace installation for projects by adding marketplace configuration to `.claude/settings.json`. When team members trust the repository folder, Claude Code prompts them to install these marketplaces and plugins.

For full configuration options including `extraKnownMarketplaces` and `enabledPlugins`, see [Plugin settings](/en/settings#plugin-settings).

## Troubleshooting

### /plugin command not recognized

If you see "unknown command" or the `/plugin` command doesn't appear:

1. **Check your version**: Run `claude --version`. Plugins require version 1.0.33 or later.
2. **Update Claude Code**:
   * **Homebrew**: `brew upgrade claude-code`
   * **npm**: `npm update -g @anthropic-ai/claude-code`
   * **Native installer**: Re-run the install command from [Setup](/en/setup)
3. **Restart Claude Code**: After updating, restart your terminal and run `claude` again.

### Common issues

* **Marketplace not loading**: Verify the URL is accessible and that `.claude-plugin/marketplace.json` exists at the path
* **Plugin installation failures**: Check that plugin source URLs are accessible and repositories are public (or you have access)
* **Files not found after installation**: Plugins are copied to a cache, so paths referencing files outside the plugin directory won't work
* **Plugin Skills not appearing**: Clear the cache with `rm -rf ~/.claude/plugins/cache`, restart Claude Code, and reinstall the plugin. See [Plugin Skills not appearing](/en/skills#plugin-skills-not-appearing-after-installation) for details.

For detailed troubleshooting with solutions, see [Troubleshooting](/en/plugin-marketplaces#troubleshooting) in the marketplace guide. For debugging tools, see [Debugging and development tools](/en/plugins-reference#debugging-and-development-tools).

## Next steps

* **Build your own plugins**: See [Plugins](/en/plugins) to create custom commands, agents, and hooks
* **Create a marketplace**: See [Create a plugin marketplace](/en/plugin-marketplaces) to distribute plugins to your team or community
* **Technical reference**: See [Plugins reference](/en/plugins-reference) for complete specifications


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt

# Agent Skills

> Create, manage, and share Skills to extend Claude's capabilities in Claude Code.

This guide shows you how to create, use, and manage Agent Skills in Claude Code. For background on how Skills work across Claude products, see [What are Skills?](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

A Skill is a markdown file that teaches Claude how to do something specific: reviewing PRs using your team's standards, generating commit messages in your preferred format, or querying your company's database schema. When you ask Claude something that matches a Skill's purpose, Claude automatically applies it.

## Create your first Skill

This example creates a personal Skill that teaches Claude to explain code using visual diagrams and analogies. Unlike Claude's default explanations, this Skill ensures every explanation includes an ASCII diagram and a real-world analogy.

<Steps>
  <Step title="Check available Skills">
    Before creating a Skill, see what Skills Claude already has access to:

    ```
    What Skills are available?
    ```

    Claude will list any Skills currently loaded. You may see none, or you may see Skills from plugins or your organization.
  </Step>

  <Step title="Create the Skill directory">
    Create a directory for the Skill in your personal Skills folder. Personal Skills are available across all your projects. (You can also create [project Skills](#where-skills-live) in `.claude/skills/` to share with your team.)

    ```bash  theme={null}
    mkdir -p ~/.claude/skills/explaining-code
    ```
  </Step>

  <Step title="Write SKILL.md">
    Every Skill needs a `SKILL.md` file. The file starts with YAML metadata between `---` markers and must include a `name` and `description`, followed by Markdown instructions that Claude follows when the Skill is active.

    The `description` is especially important, because Claude uses it to decide when to apply the Skill.

    Create `~/.claude/skills/explaining-code/SKILL.md`:

    ```yaml  theme={null}
    ---
    name: explaining-code
    description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
    ---

    When explaining code, always include:

    1. **Start with an analogy**: Compare the code to something from everyday life
    2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
    3. **Walk through the code**: Explain step-by-step what happens
    4. **Highlight a gotcha**: What's a common mistake or misconception?

    Keep explanations conversational. For complex concepts, use multiple analogies.
    ```
  </Step>

  <Step title="Load and verify the Skill">
    Exit and restart Claude Code to load the new Skill. Then verify it appears in the list:

    ```
    What Skills are available?
    ```

    You should see `explaining-code` in the list with its description.
  </Step>

  <Step title="Test the Skill">
    Open any file in your project and ask Claude a question that matches the Skill's description:

    ```
    How does this code work?
    ```

    Claude should ask to use the `explaining-code` Skill, then include an analogy and ASCII diagram in its explanation. If the Skill doesn't trigger, try rephrasing to include more keywords from the description, like "explain how this works."
  </Step>
</Steps>

The rest of this guide covers how Skills work, configuration options, and troubleshooting.

## How Skills work

Skills are **model-invoked**: Claude decides which Skills to use based on your request. You don't need to explicitly call a Skill. Claude automatically applies relevant Skills when your request matches their description.

When you send a request, Claude follows these steps to find and use relevant Skills:

<Steps>
  <Step title="Discovery">
    At startup, Claude loads only the name and description of each available Skill. This keeps startup fast while giving Claude enough context to know when each Skill might be relevant.
  </Step>

  <Step title="Activation">
    When your request matches a Skill's description, Claude asks to use the Skill. You'll see a confirmation prompt before the full `SKILL.md` is loaded into context. Claude matches requests against descriptions using semantic similarity, so [write descriptions](#skill-not-triggering) that include keywords users would naturally say.
  </Step>

  <Step title="Execution">
    Claude follows the Skill's instructions, loading referenced files or running bundled scripts as needed.
  </Step>
</Steps>

### Where Skills live

Where you store a Skill determines who can use it:

| Location   | Path                                                        | Applies to                        |
| :--------- | :---------------------------------------------------------- | :-------------------------------- |
| Enterprise | See [managed settings](/en/iam#enterprise-managed-settings) | All users in your organization    |
| Personal   | `~/.claude/skills/`                                         | You, across all projects          |
| Project    | `.claude/skills/`                                           | Anyone working in this repository |
| Plugin     | Bundled with [plugins](/en/plugins)                         | Anyone with the plugin installed  |

If two Skills have the same name, the higher row wins: enterprise overrides personal, personal overrides project, and project overrides plugin.

### When to use Skills versus other options

Claude Code offers several ways to customize behavior. The key difference: **Skills are triggered automatically by Claude** based on your request, while slash commands require you to type `/command` explicitly.

| Use this                                 | When you want to...                                                        | When it runs                               |
| :--------------------------------------- | :------------------------------------------------------------------------- | :----------------------------------------- |
| **Skills**                               | Give Claude specialized knowledge (e.g., "review PRs using our standards") | Claude chooses when relevant               |
| **[Slash commands](/en/slash-commands)** | Create reusable prompts (e.g., `/deploy staging`)                          | You type `/command` to run it              |
| **[CLAUDE.md](/en/memory)**              | Set project-wide instructions (e.g., "use TypeScript strict mode")         | Loaded into every conversation             |
| **[Subagents](/en/sub-agents)**          | Delegate tasks to a separate context with its own tools                    | Claude delegates, or you invoke explicitly |
| **[Hooks](/en/hooks)**                   | Run scripts on events (e.g., lint on file save)                            | Fires on specific tool events              |
| **[MCP servers](/en/mcp)**               | Connect Claude to external tools and data sources                          | Claude calls MCP tools as needed           |

**Skills vs. subagents**: Skills add knowledge to the current conversation. Subagents run in a separate context with their own tools. Use Skills for guidance and standards; use subagents when you need isolation or different tool access.

**Skills vs. MCP**: Skills tell Claude *how* to use tools; MCP *provides* the tools. For example, an MCP server connects Claude to your database, while a Skill teaches Claude your data model and query patterns.

<Note>
  For a deep dive into the architecture and real-world applications of Agent Skills, read [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

## Configure Skills

This section covers Skill file structure, supporting files, tool restrictions, and distribution options.

### Write SKILL.md

The `SKILL.md` file is the only required file in a Skill. It has two parts: YAML metadata (the section between `---` markers) at the top, and Markdown instructions that tell Claude how to use the Skill:

```yaml  theme={null}
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

#### Available metadata fields

You can use the following fields in the YAML frontmatter:

| Field           | Required | Description                                                                                                                                                                      |
| :-------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Skill name. Must use lowercase letters, numbers, and hyphens only (max 64 characters). Should match the directory name.                                                          |
| `description`   | Yes      | What the Skill does and when to use it (max 1024 characters). Claude uses this to decide when to apply the Skill.                                                                |
| `allowed-tools` | No       | Tools Claude can use without asking permission when this Skill is active. See [Restrict tool access](#restrict-tool-access-with-allowed-tools).                                  |
| `model`         | No       | [Model](https://docs.claude.com/en/docs/about-claude/models/overview) to use when this Skill is active (e.g., `claude-sonnet-4-20250514`). Defaults to the conversation's model. |

See the [best practices guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices) for complete authoring guidance including validation rules.

### Update or delete a Skill

To update a Skill, edit its `SKILL.md` file directly. To remove a Skill, delete its directory. Exit and restart Claude Code for changes to take effect.

### Add supporting files with progressive disclosure

Skills share Claude's context window with conversation history, other Skills, and your request. To keep context focused, use **progressive disclosure**: put essential information in `SKILL.md` and detailed reference material in separate files that Claude reads only when needed.

This approach lets you bundle comprehensive documentation, examples, and scripts without consuming context upfront. Claude loads additional files only when the task requires them.

<Tip>Keep `SKILL.md` under 500 lines for optimal performance. If your content exceeds this, split detailed reference material into separate files.</Tip>

#### Example: multi-file Skill structure

Claude discovers supporting files through links in your `SKILL.md`. The following example shows a Skill with detailed documentation in separate files and utility scripts that Claude can execute without reading:

```
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

The `SKILL.md` file references these supporting files so Claude knows they exist:

````markdown  theme={null}
## Overview

[Essential instructions here]

## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)

## Utility scripts

To validate input files, run the helper script. It checks for required fields and returns any validation errors:
```bash
python scripts/helper.py input.txt
```
````

<Tip>Keep references one level deep. Link directly from `SKILL.md` to reference files. Deeply nested references (file A links to file B which links to file C) may result in Claude partially reading files.</Tip>

**Bundle utility scripts for zero-context execution.** Scripts in your Skill directory can be executed without loading their contents into context. Claude runs the script and only the output consumes tokens. This is useful for:

* Complex validation logic that would be verbose to describe in prose
* Data processing that's more reliable as tested code than generated code
* Operations that benefit from consistency across uses

In `SKILL.md`, tell Claude to run the script rather than read it:

```markdown  theme={null}
Run the validation script to check the form:
python scripts/validate_form.py input.pdf
```

For complete guidance on structuring Skills, see the [best practices guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#progressive-disclosure-patterns).

### Restrict tool access with allowed-tools

Use the `allowed-tools` frontmatter field to limit which tools Claude can use when a Skill is active:

```yaml  theme={null}
---
name: reading-files-safely
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---

# Safe File Reader

This Skill provides read-only file access.

## Instructions
1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern
```

When this Skill is active, Claude can only use the specified tools (Read, Grep, Glob) without needing to ask for permission. This is useful for:

* Read-only Skills that shouldn't modify files
* Skills with limited scope: for example, only data analysis, no file writing
* Security-sensitive workflows where you want to restrict capabilities

If `allowed-tools` is omitted, the Skill doesn't restrict tools. Claude uses its standard permission model and may ask you to approve tool usage.

<Note>
  `allowed-tools` is only supported for Skills in Claude Code.
</Note>

### Use Skills with subagents

[Subagents](/en/sub-agents) do not automatically inherit Skills from the main conversation. To give a custom subagent access to specific Skills, list them in the subagent's `skills` field in `.claude/agents/`:

```yaml  theme={null}
# .claude/agents/code-reviewer/AGENT.md
---
name: code-reviewer
description: Review code for quality and best practices
skills: pr-review, security-check
---
```

The listed Skills are loaded into the subagent's context when it starts. If the `skills` field is omitted, no Skills are preloaded for that subagent.

<Note>
  Built-in agents (Explore, Plan, Verify) and the Task tool do not have access to your Skills. Only custom subagents you define in `.claude/agents/` with an explicit `skills` field can use Skills.
</Note>

### Distribute Skills

You can share Skills in several ways:

* **Project Skills**: Commit `.claude/skills/` to version control. Anyone who clones the repository gets the Skills.
* **Plugins**: To share Skills across multiple repositories, create a `skills/` directory in your [plugin](/en/plugins) with Skill folders containing `SKILL.md` files. Distribute through a [plugin marketplace](/en/plugin-marketplaces).
* **Enterprise**: Administrators can deploy Skills organization-wide through [managed settings](/en/iam#enterprise-managed-settings). See [Where Skills live](#where-skills-live) for enterprise Skill paths.

## Examples

These examples show common Skill patterns, from minimal single-file Skills to multi-file Skills with supporting documentation and scripts.

### Simple Skill (single file)

A minimal Skill needs only a `SKILL.md` file with frontmatter and instructions. This example helps Claude generate commit messages by examining staged changes:

```
commit-helper/
└── SKILL.md
```

```yaml  theme={null}
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices

- Use present tense
- Explain what and why, not how
```

### Use multiple files

For complex Skills, use progressive disclosure to keep the main `SKILL.md` focused while providing detailed documentation in supporting files. This PDF processing Skill includes reference docs, utility scripts, and uses `allowed-tools` to restrict Claude to specific tools:

```
pdf-processing/
├── SKILL.md              # Overview and quick start
├── FORMS.md              # Form field mappings and filling instructions
├── REFERENCE.md          # API details for pypdf and pdfplumber
└── scripts/
    ├── fill_form.py      # Utility to populate form fields
    └── validate.py       # Checks PDFs for required fields
```

**`SKILL.md`**:

````yaml  theme={null}
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
allowed-tools: Read, Bash(python:*)
---

# PDF Processing

## Quick start

Extract text:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements

Packages must be installed in your environment:
```bash
pip install pypdf pdfplumber
```
````

<Note>
  If your Skill requires external packages, list them in the description. Packages must be installed in your environment before Claude can use them.
</Note>

## Troubleshooting

### View and test Skills

To see which Skills Claude has access to, ask Claude a question like "What Skills are available?" Claude loads all available Skill names and descriptions into the context window when a conversation starts, so it can list the Skills it currently has access to.

To test a specific Skill, ask Claude to do a task that matches the Skill's description. For example, if your Skill has the description "Reviews pull requests for code quality", ask Claude to "Review the changes in my current branch." Claude automatically uses the Skill when the request matches its description.

### Skill not triggering

The description field is how Claude decides whether to use your Skill. Vague descriptions like "Helps with documents" don't give Claude enough information to match your Skill to relevant requests.

A good description answers two questions:

1. **What does this Skill do?** List the specific capabilities.
2. **When should Claude use it?** Include trigger terms users would mention.

```yaml  theme={null}
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

This description works because it names specific actions (extract, fill, merge) and includes keywords users would say (PDF, forms, document extraction).

### Skill doesn't load

**Check the file path.** Skills must be in the correct directory with the exact filename `SKILL.md` (case-sensitive):

| Type       | Path                                                                    |
| :--------- | :---------------------------------------------------------------------- |
| Personal   | `~/.claude/skills/my-skill/SKILL.md`                                    |
| Project    | `.claude/skills/my-skill/SKILL.md`                                      |
| Enterprise | See [Where Skills live](#where-skills-live) for platform-specific paths |
| Plugin     | `skills/my-skill/SKILL.md` inside the plugin directory                  |

**Check the YAML syntax.** Invalid YAML in the frontmatter prevents the Skill from loading. The frontmatter must start with `---` on line 1 (no blank lines before it), end with `---` before the Markdown content, and use spaces for indentation (not tabs).

**Run debug mode.** Use `claude --debug` to see Skill loading errors.

### Skill has errors

**Check dependencies are installed.** If your Skill uses external packages, they must be installed in your environment before Claude can use them.

**Check script permissions.** Scripts need execute permissions: `chmod +x scripts/*.py`

**Check file paths.** Use forward slashes (Unix style) in all paths. Use `scripts/helper.py`, not `scripts\helper.py`.

### Multiple Skills conflict

If Claude uses the wrong Skill or seems confused between similar Skills, the descriptions are probably too similar. Make each description distinct by using specific trigger terms.

For example, instead of two Skills with "data analysis" in both descriptions, differentiate them: one for "sales data in Excel files and CRM exports" and another for "log files and system metrics". The more specific your trigger terms, the easier it is for Claude to match the right Skill to your request.

### Plugin Skills not appearing

**Symptom**: You installed a plugin from a marketplace, but its Skills don't appear when you ask Claude "What Skills are available?"

**Solution**: Clear the plugin cache and reinstall:

```bash  theme={null}
rm -rf ~/.claude/plugins/cache
```

Then restart Claude Code and reinstall the plugin:

```shell  theme={null}
/plugin install plugin-name@marketplace-name
```

This forces Claude Code to re-download and re-register the plugin's Skills.

**If Skills still don't appear**, verify the plugin's directory structure is correct. Skills must be in a `skills/` directory at the plugin root:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

## Next steps

<CardGroup cols={2}>
  <Card title="Authoring best practices" icon="lightbulb" href="https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices">
    Write Skills that Claude can use effectively
  </Card>

  <Card title="Agent Skills overview" icon="book" href="https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview">
    Learn how Skills work across Claude products
  </Card>

  <Card title="Use Skills in the Agent SDK" icon="cube" href="https://docs.claude.com/en/docs/agent-sdk/skills">
    Use Skills programmatically with TypeScript and Python
  </Card>

  <Card title="Get started with Agent Skills" icon="rocket" href="https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart">
    Create your first Skill
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt

# Output styles

> Adapt Claude Code for uses beyond software engineering

Output styles allow you to use Claude Code as any type of agent while keeping
its core capabilities, such as running local scripts, reading/writing files, and
tracking TODOs.

## Built-in output styles

Claude Code's **Default** output style is the existing system prompt, designed
to help you complete software engineering tasks efficiently.

There are two additional built-in output styles focused on teaching you the
codebase and how Claude operates:

* **Explanatory**: Provides educational "Insights" in between helping you
  complete software engineering tasks. Helps you understand implementation
  choices and codebase patterns.

* **Learning**: Collaborative, learn-by-doing mode where Claude will not only
  share "Insights" while coding, but also ask you to contribute small, strategic
  pieces of code yourself. Claude Code will add `TODO(human)` markers in your
  code for you to implement.

## How output styles work

Output styles directly modify Claude Code's system prompt.

* All output styles exclude instructions for efficient output (such as
  responding concisely).
* Custom output styles exclude instructions for coding (such as verifying code
  with tests), unless `keep-coding-instructions` is true.
* All output styles have their own custom instructions added to the end of the
  system prompt.
* All output styles trigger reminders for Claude to adhere to the output style
  instructions during the conversation.

## Change your output style

You can either:

* Run `/output-style` to access a menu and select your output style (this can
  also be accessed from the `/config` menu)

* Run `/output-style [style]`, such as `/output-style explanatory`, to directly
  switch to a style

These changes apply to the [local project level](/en/settings) and are saved in
`.claude/settings.local.json`. You can also directly edit the `outputStyle`
field in a settings file at a different level.

## Create a custom output style

Custom output styles are Markdown files with frontmatter and the text that will
be added to the system prompt:

```markdown  theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

You can save these files at the user level (`~/.claude/output-styles`) or
project level (`.claude/output-styles`).

### Frontmatter

Output style files support frontmatter, useful for specifying metadata about the
command:

| Frontmatter                | Purpose                                                                     | Default                 |
| :------------------------- | :-------------------------------------------------------------------------- | :---------------------- |
| `name`                     | Name of the output style, if not the file name                              | Inherits from file name |
| `description`              | Description of the output style. Used only in the UI of `/output-style`     | None                    |
| `keep-coding-instructions` | Whether to keep the parts of Claude Code's system prompt related to coding. | false                   |

## Comparisons to related features

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

Output styles completely "turn off" the parts of Claude Code's default system
prompt specific to software engineering. Neither CLAUDE.md nor
`--append-system-prompt` edit Claude Code's default system prompt. CLAUDE.md
adds the contents as a user message *following* Claude Code's default system
prompt. `--append-system-prompt` appends the content to the system prompt.

### Output Styles vs. [Agents](/en/sub-agents)

Output styles directly affect the main agent loop and only affect the system
prompt. Agents are invoked to handle specific tasks and can include additional
settings like the model to use, the tools they have available, and some context
about when to use the agent.

### Output Styles vs. [Custom Slash Commands](/en/slash-commands)

You can think of output styles as "stored system prompts" and custom slash
commands as "stored prompts".


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt

# Get started with Claude Code hooks

> Learn how to customize and extend Claude Code's behavior by registering shell commands

Claude Code hooks are user-defined shell commands that execute at various points
in Claude Code's lifecycle. Hooks provide deterministic control over Claude
Code's behavior, ensuring certain actions always happen rather than relying on
the LLM to choose to run them.

<Tip>
  For reference documentation on hooks, see [Hooks reference](/en/hooks).
</Tip>

Example use cases for hooks include:

* **Notifications**: Customize how you get notified when Claude Code is awaiting
  your input or permission to run something.
* **Automatic formatting**: Run `prettier` on .ts files, `gofmt` on .go files,
  etc. after every file edit.
* **Logging**: Track and count all executed commands for compliance or
  debugging.
* **Feedback**: Provide automated feedback when Claude Code produces code that
  does not follow your codebase conventions.
* **Custom permissions**: Block modifications to production files or sensitive
  directories.

By encoding these rules as hooks rather than prompting instructions, you turn
suggestions into app-level code that executes every time it is expected to run.

<Warning>
  You must consider the security implication of hooks as you add them, because hooks run automatically during the agent loop with your current environment's credentials.
  For example, malicious hooks code can exfiltrate your data. Always review your hooks implementation before registering them.

  For full security best practices, see [Security Considerations](/en/hooks#security-considerations) in the hooks reference documentation.
</Warning>

## Hook Events Overview

Claude Code provides several hook events that run at different points in the
workflow:

* **PreToolUse**: Runs before tool calls (can block them)
* **PermissionRequest**: Runs when a permission dialog is shown (can allow or deny)
* **PostToolUse**: Runs after tool calls complete
* **UserPromptSubmit**: Runs when the user submits a prompt, before Claude processes it
* **Notification**: Runs when Claude Code sends notifications
* **Stop**: Runs when Claude Code finishes responding
* **SubagentStop**: Runs when subagent tasks complete
* **PreCompact**: Runs before Claude Code is about to run a compact operation
* **SessionStart**: Runs when Claude Code starts a new session or resumes an existing session
* **SessionEnd**: Runs when Claude Code session ends

Each event receives different data and can control Claude's behavior in
different ways.

## Quickstart

In this quickstart, you'll add a hook that logs the shell commands that Claude
Code runs.

### Prerequisites

Install `jq` for JSON processing in the command line.

### Step 1: Open hooks configuration

Run the `/hooks` [slash command](/en/slash-commands) and select
the `PreToolUse` hook event.

`PreToolUse` hooks run before tool calls and can block them while providing
Claude feedback on what to do differently.

### Step 2: Add a matcher

Select `+ Add new matcher…` to run your hook only on Bash tool calls.

Type `Bash` for the matcher.

<Note>You can use `*` to match all tools.</Note>

### Step 3: Add the hook

Select `+ Add new hook…` and enter this command:

```bash  theme={null}
jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
```

### Step 4: Save your configuration

For storage location, select `User settings` since you're logging to your home
directory. This hook will then apply to all projects, not just your current
project.

Then press `Esc` until you return to the REPL. Your hook is now registered.

### Step 5: Verify your hook

Run `/hooks` again or check `~/.claude/settings.json` to see your configuration:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Step 6: Test your hook

Ask Claude to run a simple command like `ls` and check your log file:

```bash  theme={null}
cat ~/.claude/bash-command-log.txt
```

You should see entries like:

```
ls - Lists files and directories
```

## More Examples

<Note>
  For a complete example implementation, see the [bash command validator example](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py) in our public codebase.
</Note>

### Code Formatting Hook

Automatically format TypeScript files after editing:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### Markdown Formatting Hook

Automatically fix missing language tags and formatting issues in markdown files:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/markdown_formatter.py"
          }
        ]
      }
    ]
  }
}
```

Create `.claude/hooks/markdown_formatter.py` with this content:

````python  theme={null}
#!/usr/bin/env python3
"""
Markdown formatter for Claude Code output.
Fixes missing language tags and spacing issues while preserving code content.
"""
import json
import sys
import re
import os

def detect_language(code):
    """Best-effort language detection from code content."""
    s = code.strip()
    
    # JSON detection
    if re.search(r'^\s*[{\[]', s):
        try:
            json.loads(s)
            return 'json'
        except:
            pass
    
    # Python detection
    if re.search(r'^\s*def\s+\w+\s*\(', s, re.M) or \
       re.search(r'^\s*(import|from)\s+\w+', s, re.M):
        return 'python'
    
    # JavaScript detection  
    if re.search(r'\b(function\s+\w+\s*\(|const\s+\w+\s*=)', s) or \
       re.search(r'=>|console\.(log|error)', s):
        return 'javascript'
    
    # Bash detection
    if re.search(r'^#!.*\b(bash|sh)\b', s, re.M) or \
       re.search(r'\b(if|then|fi|for|in|do|done)\b', s):
        return 'bash'
    
    # SQL detection
    if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+', s, re.I):
        return 'sql'
        
    return 'text'

def format_markdown(content):
    """Format markdown content with language detection."""
    # Fix unlabeled code fences
    def add_lang_to_fence(match):
        indent, info, body, closing = match.groups()
        if not info.strip():
            lang = detect_language(body)
            return f"{indent}```{lang}\n{body}{closing}\n"
        return match.group(0)
    
    fence_pattern = r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$'
    content = re.sub(fence_pattern, add_lang_to_fence, content)
    
    # Fix excessive blank lines (only outside code fences)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.rstrip() + '\n'

# Main execution
try:
    input_data = json.load(sys.stdin)
    file_path = input_data.get('tool_input', {}).get('file_path', '')
    
    if not file_path.endswith(('.md', '.mdx')):
        sys.exit(0)  # Not a markdown file
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        formatted = format_markdown(content)
        
        if formatted != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"✓ Fixed markdown formatting in {file_path}")
    
except Exception as e:
    print(f"Error formatting markdown: {e}", file=sys.stderr)
    sys.exit(1)
````

Make the script executable:

```bash  theme={null}
chmod +x .claude/hooks/markdown_formatter.py
```

This hook automatically:

* Detects programming languages in unlabeled code blocks
* Adds appropriate language tags for syntax highlighting
* Fixes excessive blank lines while preserving code content
* Only processes markdown files (`.md`, `.mdx`)

### Custom Notification Hook

Get desktop notifications when Claude needs input:

```json  theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### File Protection Hook

Block edits to sensitive files:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

## Learn more

* For reference documentation on hooks, see [Hooks reference](/en/hooks).
* For comprehensive security best practices and safety guidelines, see [Security Considerations](/en/hooks#security-considerations) in the hooks reference documentation.
* For troubleshooting steps and debugging techniques, see [Debugging](/en/hooks#debugging) in the hooks reference
  documentation.


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt