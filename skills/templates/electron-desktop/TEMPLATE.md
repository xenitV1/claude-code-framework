---
name: electron-desktop
description: Cross-platform desktop application template with Electron, React, and TypeScript.
---

# Electron Desktop App Template

## Tech Stack

- **Framework:** Electron 28+
- **UI:** React 18
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Bundler:** Vite + electron-builder
- **IPC:** Type-safe IPC communication

---

## Directory Structure

```
project-name/
├── electron/
│   ├── main.ts                  # Main process
│   ├── preload.ts               # Preload script
│   └── ipc/
│       └── handlers.ts          # IPC handlers
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── components/
│   │   ├── TitleBar.tsx
│   │   └── Sidebar.tsx
│   ├── hooks/
│   │   └── useElectron.ts
│   ├── lib/
│   │   └── ipc.ts
│   └── styles/
│       └── globals.css
├── public/
│   └── icon.png
├── package.json
├── electron-builder.json
├── vite.config.ts
└── tsconfig.json
```

---

## Core Files

### package.json

```json
{
  "name": "{{PROJECT_NAME}}",
  "version": "1.0.0",
  "main": "dist-electron/main.js",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build && electron-builder",
    "preview": "vite preview",
    "electron:dev": "concurrently \"vite\" \"wait-on http://localhost:5173 && electron .\"",
    "electron:build": "vite build && electron-builder"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "concurrently": "^8.2.0",
    "electron": "^28.0.0",
    "electron-builder": "^24.9.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vite-plugin-electron": "^0.28.0",
    "vite-plugin-electron-renderer": "^0.14.0",
    "wait-on": "^7.2.0"
  }
}
```

### electron/main.ts

```typescript
import { app, BrowserWindow, ipcMain } from 'electron';
import { join } from 'path';
import { registerIpcHandlers } from './ipc/handlers';

let mainWindow: BrowserWindow | null = null;

const isDev = process.env.NODE_ENV === 'development';

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    frame: false, // Custom title bar
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(join(__dirname, '../dist/index.html'));
  }

  // Window controls
  ipcMain.on('window:minimize', () => mainWindow?.minimize());
  ipcMain.on('window:maximize', () => {
    if (mainWindow?.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow?.maximize();
    }
  });
  ipcMain.on('window:close', () => mainWindow?.close());
}

app.whenReady().then(() => {
  registerIpcHandlers();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
```

### electron/preload.ts

```typescript
import { contextBridge, ipcRenderer } from 'electron';

const electronAPI = {
  // Window controls
  minimize: () => ipcRenderer.send('window:minimize'),
  maximize: () => ipcRenderer.send('window:maximize'),
  close: () => ipcRenderer.send('window:close'),

  // File system
  readFile: (path: string) => ipcRenderer.invoke('fs:readFile', path),
  writeFile: (path: string, data: string) => 
    ipcRenderer.invoke('fs:writeFile', path, data),
  selectFile: () => ipcRenderer.invoke('dialog:openFile'),
  selectFolder: () => ipcRenderer.invoke('dialog:openFolder'),

  // App info
  getVersion: () => ipcRenderer.invoke('app:version'),

  // Events
  onUpdate: (callback: (info: unknown) => void) => {
    ipcRenderer.on('app:update', (_, info) => callback(info));
  },
};

contextBridge.exposeInMainWorld('electron', electronAPI);

// Type declaration for renderer
declare global {
  interface Window {
    electron: typeof electronAPI;
  }
}
```

### electron/ipc/handlers.ts

```typescript
import { ipcMain, dialog, app } from 'electron';
import { readFile, writeFile } from 'fs/promises';

export function registerIpcHandlers() {
  // File operations
  ipcMain.handle('fs:readFile', async (_, path: string) => {
    try {
      return await readFile(path, 'utf-8');
    } catch (error) {
      throw new Error(`Failed to read file: ${path}`);
    }
  });

  ipcMain.handle('fs:writeFile', async (_, path: string, data: string) => {
    try {
      await writeFile(path, data, 'utf-8');
      return true;
    } catch (error) {
      throw new Error(`Failed to write file: ${path}`);
    }
  });

  // Dialogs
  ipcMain.handle('dialog:openFile', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [
        { name: 'All Files', extensions: ['*'] },
        { name: 'Text', extensions: ['txt', 'md'] },
        { name: 'JSON', extensions: ['json'] },
      ],
    });
    return result.canceled ? null : result.filePaths[0];
  });

  ipcMain.handle('dialog:openFolder', async () => {
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory'],
    });
    return result.canceled ? null : result.filePaths[0];
  });

  // App info
  ipcMain.handle('app:version', () => app.getVersion());
}
```

### src/components/TitleBar.tsx

```tsx
import { Minus, Square, X } from 'lucide-react';

export function TitleBar() {
  return (
    <div className="h-8 bg-slate-900 flex items-center justify-between select-none drag">
      <div className="flex items-center gap-2 px-4">
        <img src="/icon.png" alt="Logo" className="w-4 h-4" />
        <span className="text-sm text-white font-medium">{{PROJECT_NAME}}</span>
      </div>
      
      <div className="flex no-drag">
        <button
          onClick={() => window.electron.minimize()}
          className="w-12 h-8 flex items-center justify-center hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
        >
          <Minus size={16} />
        </button>
        <button
          onClick={() => window.electron.maximize()}
          className="w-12 h-8 flex items-center justify-center hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
        >
          <Square size={14} />
        </button>
        <button
          onClick={() => window.electron.close()}
          className="w-12 h-8 flex items-center justify-center hover:bg-red-600 text-slate-400 hover:text-white transition-colors"
        >
          <X size={16} />
        </button>
      </div>
    </div>
  );
}
```

### src/App.tsx

```tsx
import { useState } from 'react';
import { TitleBar } from './components/TitleBar';

export default function App() {
  const [file, setFile] = useState<string | null>(null);
  const [content, setContent] = useState('');

  const handleOpen = async () => {
    const path = await window.electron.selectFile();
    if (path) {
      setFile(path);
      const data = await window.electron.readFile(path);
      setContent(data);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-slate-800">
      <TitleBar />
      
      <main className="flex-1 p-6 overflow-auto">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-white mb-6">
            Welcome to {{PROJECT_NAME}}
          </h1>
          
          <button
            onClick={handleOpen}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Open File
          </button>
          
          {file && (
            <div className="mt-6">
              <p className="text-slate-400 text-sm mb-2">{file}</p>
              <pre className="bg-slate-900 p-4 rounded-lg text-slate-300 overflow-auto">
                {content}
              </pre>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
```

### electron-builder.json

```json
{
  "appId": "com.{{BUNDLE_ID}}.app",
  "productName": "{{PROJECT_NAME}}",
  "directories": {
    "output": "release"
  },
  "files": [
    "dist/**/*",
    "dist-electron/**/*"
  ],
  "win": {
    "target": ["nsis", "portable"],
    "icon": "public/icon.png"
  },
  "mac": {
    "target": ["dmg", "zip"],
    "icon": "public/icon.png"
  },
  "linux": {
    "target": ["AppImage", "deb"],
    "icon": "public/icon.png"
  }
}
```

---

## Setup Steps

1. `npm create vite {{name}} -- --template react-ts`
2. `cd {{name}}`
3. Install: `npm install && npm install -D electron electron-builder vite-plugin-electron concurrently wait-on`
4. Copy template files
5. `npm run electron:dev`

---

## Build for Production

```bash
# Windows
npm run electron:build -- --win

# macOS
npm run electron:build -- --mac

# Linux
npm run electron:build -- --linux
```
