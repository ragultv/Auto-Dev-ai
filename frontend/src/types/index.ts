export interface User {
  id: string;
  name: string;
  email: string;
  apiKeys: {
    openai?: string;
    anthropic?: string;
    gemini?: string;
    api?: string;
  };
  access_token?: string;
  refresh_token?: string;
}

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  model?: string;
}

export interface FileItem {
  id: string;
  name: string;
  type: 'file' | 'folder';
  content?: string;
  children?: FileItem[];
  path: string;
}

export interface Project {
  id: string;
  name: string;
  files: FileItem[];
  createdAt: Date;
}

export type AIModel = 'gpt-4' | 'claude-3' | 'gemini-pro';