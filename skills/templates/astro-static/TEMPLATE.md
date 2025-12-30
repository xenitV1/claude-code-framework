---
name: astro-static
description: Astro static site template for content-focused websites, blogs, and documentation.
---

# Astro Static Site Template

## Tech Stack

- **Framework:** Astro 4.x
- **Content:** MDX + Content Collections
- **Styling:** Tailwind CSS
- **Integrations:** Sitemap, RSS, SEO
- **Deployment:** Static/SSG

---

## Directory Structure

```
project-name/
├── src/
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── Navigation.astro
│   │   ├── Card.astro
│   │   └── TOC.astro
│   ├── content/
│   │   ├── blog/
│   │   │   ├── first-post.mdx
│   │   │   └── second-post.mdx
│   │   ├── docs/
│   │   │   └── getting-started.mdx
│   │   └── config.ts
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   ├── BlogLayout.astro
│   │   └── DocsLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── about.astro
│   │   ├── blog/
│   │   │   ├── index.astro
│   │   │   └── [...slug].astro
│   │   ├── docs/
│   │   │   └── [...slug].astro
│   │   └── rss.xml.ts
│   └── styles/
│       └── global.css
├── public/
│   ├── favicon.svg
│   └── og-image.png
├── astro.config.mjs
├── tailwind.config.mjs
├── package.json
└── tsconfig.json
```

---

## Core Files

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "type": "module",
  "version": "0.0.1",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "astro": "^4.4.0",
    "@astrojs/mdx": "^2.1.0",
    "@astrojs/sitemap": "^3.0.0",
    "@astrojs/tailwind": "^5.1.0",
    "@astrojs/rss": "^4.0.0",
    "tailwindcss": "^3.4.0"
  }
}
```

### astro.config.mjs

```javascript
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://{{DOMAIN}}',
  integrations: [
    mdx(),
    sitemap(),
    tailwind(),
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});
```

### src/content/config.ts

```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const docs = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    order: z.number().default(0),
  }),
});

export const collections = { blog, docs };
```

### src/layouts/BaseLayout.astro

```astro
---
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';
import '../styles/global.css';

interface Props {
  title: string;
  description?: string;
  image?: string;
}

const { title, description = '{{PROJECT_DESCRIPTION}}', image = '/og-image.png' } = Astro.props;
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="canonical" href={canonicalURL} />
    
    <title>{title} | {{PROJECT_NAME}}</title>
    <meta name="description" content={description} />
    
    <!-- Open Graph -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content={canonicalURL} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={new URL(image, Astro.url)} />
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image" />
    <meta property="twitter:url" content={canonicalURL} />
    <meta property="twitter:title" content={title} />
    <meta property="twitter:description" content={description} />
    <meta property="twitter:image" content={new URL(image, Astro.url)} />
  </head>
  <body class="min-h-screen bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
    <Header />
    <main>
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

### src/pages/index.astro

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Card from '../components/Card.astro';
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog'))
  .filter((post) => !post.data.draft)
  .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf())
  .slice(0, 3);
---

<BaseLayout title="Home">
  <!-- Hero -->
  <section class="py-24 px-6 bg-gradient-to-b from-slate-900 to-slate-800 text-white">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-5xl font-bold mb-6">
        Welcome to <span class="text-blue-400">{{PROJECT_NAME}}</span>
      </h1>
      <p class="text-xl text-slate-300 mb-8">
        {{PROJECT_DESCRIPTION}}
      </p>
      <div class="flex gap-4 justify-center">
        <a href="/docs" class="px-6 py-3 bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
          Get Started
        </a>
        <a href="/blog" class="px-6 py-3 border border-slate-600 rounded-lg hover:bg-slate-800 transition-colors">
          Read Blog
        </a>
      </div>
    </div>
  </section>

  <!-- Latest Posts -->
  <section class="py-16 px-6">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-3xl font-bold mb-8">Latest Posts</h2>
      <div class="grid md:grid-cols-3 gap-6">
        {posts.map((post) => (
          <Card
            title={post.data.title}
            description={post.data.description}
            href={`/blog/${post.slug}`}
            date={post.data.pubDate}
          />
        ))}
      </div>
    </div>
  </section>
</BaseLayout>
```

### src/pages/blog/[...slug].astro

```astro
---
import { getCollection, type CollectionEntry } from 'astro:content';
import BlogLayout from '../../layouts/BlogLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: post,
  }));
}

type Props = CollectionEntry<'blog'>;

const post = Astro.props;
const { Content } = await post.render();
---

<BlogLayout {...post.data}>
  <Content />
</BlogLayout>
```

### src/pages/rss.xml.ts

```typescript
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getCollection('blog');
  
  return rss({
    title: '{{PROJECT_NAME}}',
    description: '{{PROJECT_DESCRIPTION}}',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.slug}/`,
    })),
  });
}
```

### src/components/Card.astro

```astro
---
interface Props {
  title: string;
  description: string;
  href: string;
  date?: Date;
}

const { title, description, href, date } = Astro.props;
---

<a href={href} class="block p-6 bg-slate-50 dark:bg-slate-800 rounded-xl hover:shadow-lg transition-shadow">
  {date && (
    <time datetime={date.toISOString()} class="text-sm text-slate-500">
      {date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}
    </time>
  )}
  <h3 class="text-xl font-semibold mt-2 mb-2">{title}</h3>
  <p class="text-slate-600 dark:text-slate-400">{description}</p>
</a>
```

### src/content/blog/first-post.mdx

```mdx
---
title: "First Blog Post"
description: "This is my first blog post using Astro."
pubDate: 2024-01-15
tags: ["astro", "blogging"]
---

# Hello World

This is my first blog post!

## Features

- Fast by default
- Content collections
- MDX support

```javascript
console.log('Hello, Astro!');
```
```

---

## Setup Steps

1. `npm create astro@latest {{name}}`
2. `cd {{name}}`
3. Add integrations: `npx astro add mdx tailwind sitemap`
4. Copy template files
5. `npm run dev`

---

## Deployment

```bash
# Build static site
npm run build

# Preview locally
npm run preview

# Deploy to Vercel/Netlify/Cloudflare Pages
# Just connect your repo - auto-detected!
```
