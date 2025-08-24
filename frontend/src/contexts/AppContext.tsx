import React, { createContext, useContext, useState } from 'react';
import { ChatMessage, Project, FileItem, AIModel } from '../types';

interface AppContextType {
  // Chat state
  messages: ChatMessage[];
  currentModel: AIModel;
  setCurrentModel: (model: AIModel) => void;
  addMessage: (content: string, sender: 'user' | 'ai', model?: string) => void;
  
  // Project state
  currentProject: Project | null;
  setCurrentProject: (project: Project) => void;
  currentFile: FileItem | null;
  setCurrentFile: (file: FileItem | null) => void;
  
  // UI state
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  chatWidth: number;
  setChatWidth: (width: number) => void;
  activeTab: 'editor' | 'preview' | 'terminal';
  setActiveTab: (tab: 'editor' | 'preview' | 'terminal') => void;
  showPromptArea: boolean;
  setShowPromptArea: (show: boolean) => void;
  resetToPrompt: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentModel, setCurrentModel] = useState<AIModel>('gpt-4');
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [currentFile, setCurrentFile] = useState<FileItem | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [chatWidth, setChatWidth] = useState(30);
  const [activeTab, setActiveTab] = useState<'editor' | 'preview' | 'terminal'>('editor');
  const [showPromptArea, setShowPromptArea] = useState(true);

  const addMessage = (content: string, sender: 'user' | 'ai', model?: string) => {
    const message: ChatMessage = {
      id: Date.now().toString(),
      content,
      sender,
      timestamp: new Date(),
      model
    };
    setMessages(prev => [...prev, message]);
    
    // Hide prompt area after first message
    if (sender === 'user' && showPromptArea) {
      setShowPromptArea(false);
    }
  };

  const resetToPrompt = () => {
    setShowPromptArea(true);
    setMessages([]);
    setCurrentProject(null);
    setCurrentFile(null);
  };

  return (
    <AppContext.Provider value={{
      messages,
      currentModel,
      setCurrentModel,
      addMessage,
      currentProject,
      setCurrentProject,
      currentFile,
      setCurrentFile,
      sidebarOpen,
      setSidebarOpen,
      chatWidth,
      setChatWidth,
      activeTab,
      setActiveTab,
      showPromptArea,
      setShowPromptArea,
      resetToPrompt
    }}>
      {children}
    </AppContext.Provider>
  );
};