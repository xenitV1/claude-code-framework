---
name: cli-tool
description: Node.js CLI tool template with Commander.js, interactive prompts, and beautiful output.
---

# CLI Tool Template

## Tech Stack

- **Runtime:** Node.js 20+
- **Language:** TypeScript
- **CLI Framework:** Commander.js
- **Prompts:** Inquirer.js
- **Output:** chalk + ora
- **Config:** cosmiconfig

---

## Directory Structure

```
project-name/
├── src/
│   ├── index.ts                 # Entry point
│   ├── cli.ts                   # CLI setup
│   ├── commands/
│   │   ├── init.ts
│   │   ├── generate.ts
│   │   └── config.ts
│   ├── lib/
│   │   ├── config.ts            # Config loader
│   │   ├── logger.ts            # Styled output
│   │   └── utils.ts
│   └── types/
│       └── index.ts
├── bin/
│   └── cli.js                   # Executable
├── package.json
├── tsconfig.json
└── README.md
```

---

## Core Files

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "description": "{{PROJECT_DESCRIPTION}}",
  "type": "module",
  "bin": {
    "{{CLI_NAME}}": "./bin/cli.js"
  },
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "link": "npm link"
  },
  "dependencies": {
    "commander": "^12.0.0",
    "@inquirer/prompts": "^4.0.0",
    "chalk": "^5.3.0",
    "ora": "^8.0.0",
    "cosmiconfig": "^9.0.0",
    "fs-extra": "^11.2.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/fs-extra": "^11.0.0",
    "@types/node": "^20.0.0",
    "tsx": "^4.7.0",
    "typescript": "^5.3.0"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

### bin/cli.js

```javascript
#!/usr/bin/env node
import '../dist/index.js';
```

### src/index.ts

```typescript
import { cli } from './cli.js';

cli.parse(process.argv);
```

### src/cli.ts

```typescript
import { Command } from 'commander';
import { initCommand } from './commands/init.js';
import { generateCommand } from './commands/generate.js';
import { configCommand } from './commands/config.js';

export const cli = new Command();

cli
  .name('{{CLI_NAME}}')
  .description('{{PROJECT_DESCRIPTION}}')
  .version('1.0.0');

cli.addCommand(initCommand);
cli.addCommand(generateCommand);
cli.addCommand(configCommand);

// Default action
cli.action(() => {
  cli.help();
});
```

### src/commands/init.ts

```typescript
import { Command } from 'commander';
import { input, select, confirm } from '@inquirer/prompts';
import { logger } from '../lib/logger.js';
import { writeFile, ensureDir } from 'fs-extra';
import { join } from 'path';
import ora from 'ora';

export const initCommand = new Command('init')
  .description('Initialize a new project')
  .argument('[name]', 'Project name')
  .option('-t, --template <template>', 'Template to use', 'default')
  .option('-y, --yes', 'Skip prompts and use defaults')
  .action(async (name, options) => {
    logger.title('Project Initialization');

    // Get project name
    const projectName = name || await input({
      message: 'Project name:',
      default: 'my-project',
    });

    // Get template
    const template = options.yes ? options.template : await select({
      message: 'Select a template:',
      choices: [
        { name: 'Default', value: 'default' },
        { name: 'Minimal', value: 'minimal' },
        { name: 'Full', value: 'full' },
      ],
    });

    // Confirm
    if (!options.yes) {
      const proceed = await confirm({
        message: `Create project "${projectName}" with ${template} template?`,
        default: true,
      });
      if (!proceed) {
        logger.warn('Aborted');
        return;
      }
    }

    // Create project
    const spinner = ora('Creating project...').start();

    try {
      const projectDir = join(process.cwd(), projectName);
      await ensureDir(projectDir);

      // Create config file
      const config = {
        name: projectName,
        template,
        version: '1.0.0',
      };
      await writeFile(
        join(projectDir, '{{CLI_NAME}}.config.json'),
        JSON.stringify(config, null, 2)
      );

      spinner.succeed('Project created successfully!');
      logger.success(`\nNext steps:`);
      logger.info(`  cd ${projectName}`);
      logger.info(`  {{CLI_NAME}} generate`);
    } catch (error) {
      spinner.fail('Failed to create project');
      logger.error(error instanceof Error ? error.message : 'Unknown error');
      process.exit(1);
    }
  });
```

### src/commands/generate.ts

```typescript
import { Command } from 'commander';
import { input, select } from '@inquirer/prompts';
import { logger } from '../lib/logger.js';
import { loadConfig } from '../lib/config.js';
import ora from 'ora';

export const generateCommand = new Command('generate')
  .alias('g')
  .description('Generate a new component')
  .argument('<type>', 'Type to generate (component, page, api)')
  .argument('[name]', 'Name of the item')
  .option('-d, --dry-run', 'Show what would be generated')
  .action(async (type, name, options) => {
    const config = await loadConfig();
    
    if (!config) {
      logger.error('No config found. Run "{{CLI_NAME}} init" first.');
      process.exit(1);
    }

    const itemName = name || await input({
      message: `${type} name:`,
    });

    logger.title(`Generating ${type}: ${itemName}`);

    if (options.dryRun) {
      logger.info('Dry run - no files will be created');
      logger.info(`Would create: src/${type}s/${itemName}.ts`);
      return;
    }

    const spinner = ora(`Generating ${type}...`).start();

    // Simulate generation
    await new Promise((resolve) => setTimeout(resolve, 1000));

    spinner.succeed(`${type} "${itemName}" generated!`);
    logger.info(`Created: src/${type}s/${itemName}.ts`);
  });
```

### src/lib/logger.ts

```typescript
import chalk from 'chalk';

export const logger = {
  title: (message: string) => {
    console.log();
    console.log(chalk.bold.blue(`◆ ${message}`));
    console.log();
  },

  success: (message: string) => {
    console.log(chalk.green(`✔ ${message}`));
  },

  error: (message: string) => {
    console.log(chalk.red(`✖ ${message}`));
  },

  warn: (message: string) => {
    console.log(chalk.yellow(`⚠ ${message}`));
  },

  info: (message: string) => {
    console.log(chalk.gray(`  ${message}`));
  },

  step: (step: number, total: number, message: string) => {
    console.log(chalk.cyan(`[${step}/${total}]`) + ` ${message}`);
  },

  table: (data: Record<string, string>) => {
    const maxKeyLength = Math.max(...Object.keys(data).map((k) => k.length));
    Object.entries(data).forEach(([key, value]) => {
      console.log(`  ${chalk.gray(key.padEnd(maxKeyLength))}  ${value}`);
    });
  },
};
```

### src/lib/config.ts

```typescript
import { cosmiconfig } from 'cosmiconfig';
import { z } from 'zod';

const configSchema = z.object({
  name: z.string(),
  template: z.string().default('default'),
  version: z.string().default('1.0.0'),
  options: z.record(z.unknown()).optional(),
});

export type Config = z.infer<typeof configSchema>;

export async function loadConfig(): Promise<Config | null> {
  const explorer = cosmiconfig('{{CLI_NAME}}');
  const result = await explorer.search();

  if (!result || result.isEmpty) {
    return null;
  }

  return configSchema.parse(result.config);
}

export async function loadConfigOrThrow(): Promise<Config> {
  const config = await loadConfig();
  if (!config) {
    throw new Error('Configuration not found');
  }
  return config;
}
```

---

## Usage Examples

```bash
# Initialize a new project
{{CLI_NAME}} init my-project

# Generate a component
{{CLI_NAME}} generate component Button
{{CLI_NAME}} g page Home --dry-run

# View/edit config
{{CLI_NAME}} config get
{{CLI_NAME}} config set template full
```

---

## Setup Steps

1. `mkdir {{name}} && cd {{name}}`
2. `npm init -y`
3. Install deps: `npm install commander @inquirer/prompts chalk ora cosmiconfig fs-extra zod`
4. Install dev deps: `npm install -D typescript tsx @types/node @types/fs-extra`
5. Copy template files
6. `chmod +x bin/cli.js`
7. `npm link` (for local testing)
8. `{{CLI_NAME}} --help`

---

## Publishing to npm

```bash
npm login
npm publish
```
