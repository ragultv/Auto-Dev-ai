import React from 'react';
import { Header } from './Layout/Header';
import { ResizableLayout } from './Layout/ResizableLayout';
import { ChatArea } from './Chat/ChatArea';
import { useApp } from '../contexts/AppContext';

export const Workspace: React.FC = () => {
  const { showPromptArea } = useApp();

  // Show full-screen chat when user first logs in
  if (showPromptArea) {
    return (
      <div className="h-screen bg-gray-50">
        <ChatArea />
      </div>
    );
  }

  // Show regular workspace after first message
  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header />
      <div className="flex-1">
        <ResizableLayout />
      </div>
    </div>
  );
};