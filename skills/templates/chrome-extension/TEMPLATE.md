---
name: chrome-extension
description: Chrome Extension template with Manifest V3, React, TypeScript, and Tailwind CSS.
---

# Chrome Extension Template

## Tech Stack

- **Manifest:** V3
- **UI Framework:** React 18
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Bundler:** Vite
- **Storage:** Chrome Storage API

---

## Directory Structure

```
project-name/
├── src/
│   ├── popup/
│   │   ├── Popup.tsx            # Popup UI
│   │   ├── index.tsx            # Popup entry
│   │   └── index.html
│   ├── options/
│   │   ├── Options.tsx          # Options page
│   │   ├── index.tsx
│   │   └── index.html
│   ├── background/
│   │   └── index.ts             # Service worker
│   ├── content/
│   │   └── index.ts             # Content script
│   ├── components/
│   │   ├── Button.tsx
│   │   └── Card.tsx
│   ├── hooks/
│   │   └── useStorage.ts
│   ├── lib/
│   │   ├── storage.ts           # Chrome storage helpers
│   │   └── messaging.ts         # Message passing
│   ├── types/
│   │   └── index.ts
│   └── styles/
│       └── globals.css
├── public/
│   ├── icons/
│   │   ├── icon-16.png
│   │   ├── icon-48.png
│   │   └── icon-128.png
│   └── manifest.json
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

---

## Core Files

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite build --watch --mode development",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/chrome": "^0.0.260",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### public/manifest.json

```json
{
  "manifest_version": 3,
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "description": "{{PROJECT_DESCRIPTION}}",
  "permissions": [
    "storage",
    "activeTab",
    "scripting"
  ],
  "host_permissions": [
    "<all_urls>"
  ],
  "action": {
    "default_popup": "popup/index.html",
    "default_icon": {
      "16": "icons/icon-16.png",
      "48": "icons/icon-48.png",
      "128": "icons/icon-128.png"
    }
  },
  "options_page": "options/index.html",
  "background": {
    "service_worker": "background/index.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content/index.js"],
      "css": ["content/styles.css"]
    }
  ],
  "icons": {
    "16": "icons/icon-16.png",
    "48": "icons/icon-48.png",
    "128": "icons/icon-128.png"
  }
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        popup: resolve(__dirname, 'src/popup/index.html'),
        options: resolve(__dirname, 'src/options/index.html'),
        background: resolve(__dirname, 'src/background/index.ts'),
        content: resolve(__dirname, 'src/content/index.ts'),
      },
      output: {
        entryFileNames: '[name]/index.js',
        chunkFileNames: 'chunks/[name].[hash].js',
        assetFileNames: 'assets/[name].[ext]',
      },
    },
  },
});
```

### src/popup/Popup.tsx

```tsx
import { useState, useEffect } from 'react';
import { getStorage, setStorage } from '../lib/storage';
import { Button } from '../components/Button';

export function Popup() {
  const [enabled, setEnabled] = useState(false);
  const [count, setCount] = useState(0);

  useEffect(() => {
    getStorage(['enabled', 'count']).then((data) => {
      setEnabled(data.enabled ?? false);
      setCount(data.count ?? 0);
    });
  }, []);

  const toggleEnabled = async () => {
    const newValue = !enabled;
    setEnabled(newValue);
    await setStorage({ enabled: newValue });
    
    // Send message to content script
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab.id) {
      chrome.tabs.sendMessage(tab.id, { type: 'TOGGLE', enabled: newValue });
    }
  };

  return (
    <div className="w-80 p-4 bg-slate-900 text-white">
      <h1 className="text-xl font-bold mb-4">{{PROJECT_NAME}}</h1>
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span>Status</span>
          <span className={enabled ? 'text-green-400' : 'text-red-400'}>
            {enabled ? 'Active' : 'Inactive'}
          </span>
        </div>
        
        <div className="flex items-center justify-between">
          <span>Usage Count</span>
          <span className="text-blue-400">{count}</span>
        </div>
        
        <Button onClick={toggleEnabled} variant={enabled ? 'secondary' : 'primary'}>
          {enabled ? 'Disable' : 'Enable'}
        </Button>
      </div>
    </div>
  );
}
```

### src/background/index.ts

```typescript
// Service Worker - runs in background

chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
  chrome.storage.local.set({ enabled: false, count: 0 });
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'INCREMENT_COUNT') {
    chrome.storage.local.get(['count'], (data) => {
      const newCount = (data.count || 0) + 1;
      chrome.storage.local.set({ count: newCount });
      sendResponse({ count: newCount });
    });
    return true; // Keep channel open for async response
  }
});

// Context menu example
chrome.contextMenus.create({
  id: 'myExtension',
  title: '{{PROJECT_NAME}}',
  contexts: ['selection'],
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'myExtension' && info.selectionText) {
    console.log('Selected text:', info.selectionText);
  }
});
```

### src/content/index.ts

```typescript
// Content Script - runs on web pages

console.log('{{PROJECT_NAME}} content script loaded');

// Listen for messages from popup/background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'TOGGLE') {
    if (message.enabled) {
      activateFeature();
    } else {
      deactivateFeature();
    }
    sendResponse({ success: true });
  }
  return true;
});

function activateFeature() {
  // Add your feature logic here
  document.body.style.border = '2px solid #22c55e';
  
  // Increment usage count
  chrome.runtime.sendMessage({ type: 'INCREMENT_COUNT' });
}

function deactivateFeature() {
  document.body.style.border = '';
}

// Initialize based on stored state
chrome.storage.local.get(['enabled'], (data) => {
  if (data.enabled) {
    activateFeature();
  }
});
```

### src/lib/storage.ts

```typescript
type StorageData = {
  enabled?: boolean;
  count?: number;
  settings?: Record<string, unknown>;
};

export function getStorage<K extends keyof StorageData>(
  keys: K[]
): Promise<Pick<StorageData, K>> {
  return new Promise((resolve) => {
    chrome.storage.local.get(keys, (data) => {
      resolve(data as Pick<StorageData, K>);
    });
  });
}

export function setStorage(data: Partial<StorageData>): Promise<void> {
  return new Promise((resolve) => {
    chrome.storage.local.set(data, resolve);
  });
}

export function onStorageChange(
  callback: (changes: { [key: string]: chrome.storage.StorageChange }) => void
) {
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === 'local') {
      callback(changes);
    }
  });
}
```

---

## Setup Steps

1. `npm create vite {{name}} -- --template react-ts`
2. `cd {{name}}`
3. Install deps: `npm install`
4. Add Chrome types: `npm install -D @types/chrome`
5. Copy template files
6. `npm run dev` (watches for changes)
7. Load in Chrome: `chrome://extensions` → Load unpacked → select `dist` folder

---

## Development Tips

1. **Hot Reload**: Use `npm run dev` for auto-rebuild
2. **Debug Popup**: Right-click extension icon → Inspect popup
3. **Debug Background**: Extensions page → Service worker link
4. **Debug Content**: DevTools on any page → Console
5. **Storage Viewer**: Extensions page → Details → Storage
