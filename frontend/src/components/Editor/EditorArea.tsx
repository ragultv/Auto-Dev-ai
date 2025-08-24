import React from 'react';
import { useApp } from '../../contexts/AppContext';
import { FileSidebar } from './FileSidebar';
import { MonacoEditor } from './MonacoEditor';
import { PreviewPanel } from './PreviewPanel';
import { TerminalPanel } from './TerminalPanel';
import { 
  Sidebar, 
  Code, 
  Eye, 
  Terminal,
  Maximize2
} from 'lucide-react';

export const EditorArea: React.FC = () => {
  const { 
    sidebarOpen, 
    setSidebarOpen, 
    activeTab, 
    setActiveTab 
  } = useApp();

  const tabs = [
    { id: 'editor' as const, label: 'Editor', icon: Code },
    { id: 'preview' as const, label: 'Preview', icon: Eye },
    { id: 'terminal' as const, label: 'Terminal', icon: Terminal }
  ];

  const renderActivePanel = () => {
    switch (activeTab) {
      case 'editor':
        return <MonacoEditor />;
      case 'preview':
        return <PreviewPanel />;
      case 'terminal':
        return <TerminalPanel />;
      default:
        return <MonacoEditor />;
    }
  };

  return (
    <div className="h-full flex bg-gray-100">
      {/* File Sidebar */}
      <FileSidebar />

      {/* Main Editor Area */}
      <div className="flex-1 flex flex-col">
        {/* Editor Header */}
        <div className="bg-white border-b border-gray-200 flex items-center justify-between px-4 py-2">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-1.5 hover:bg-gray-100 rounded transition-colors"
              title="Toggle sidebar"
            >
              <Sidebar className="w-4 h-4 text-gray-600" />
            </button>

            {/* Tabs */}
            <div className="flex items-center space-x-1">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                      activeTab === tab.id
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button className="p-1.5 hover:bg-gray-100 rounded transition-colors">
              <Maximize2 className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Active Panel */}
        <div className="flex-1">
          {renderActivePanel()}
        </div>
      </div>
    </div>
  );
};