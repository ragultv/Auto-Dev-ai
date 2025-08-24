import React, { useState } from 'react';
import { useApp } from '../../contexts/AppContext';
import { Folder, File, Plus, FolderPlus, ChevronRight, ChevronDown, Phone as Python } from 'lucide-react';
import { FileItem } from '../../types';

const mockFiles: FileItem[] = [
  {
    id: '1',
    name: 'main.py',
    type: 'file',
    path: '/main.py',
    content: `#!/usr/bin/env python3
"""
Main application entry point
"""

def main():
    print("Hello, AI Development Agent!")
    
    # Your code here
    pass

if __name__ == "__main__":
    main()
`
  },
  {
    id: '2',
    name: 'utils',
    type: 'folder',
    path: '/utils',
    children: [
      {
        id: '3',
        name: 'helpers.py',
        type: 'file',
        path: '/utils/helpers.py',
        content: `"""
Utility functions for the application
"""

def format_output(data):
    """Format data for display"""
    return str(data)

def validate_input(input_data):
    """Validate user input"""
    return input_data is not None
`
      }
    ]
  },
  {
    id: '4',
    name: 'requirements.txt',
    type: 'file',
    path: '/requirements.txt',
    content: `# Python dependencies
requests>=2.28.0
numpy>=1.24.0
pandas>=2.0.0
`
  }
];

interface FileTreeItemProps {
  item: FileItem;
  level: number;
  onSelect: (file: FileItem) => void;
  selectedFile: FileItem | null;
}

const FileTreeItem: React.FC<FileTreeItemProps> = ({ item, level, onSelect, selectedFile }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const handleClick = () => {
    if (item.type === 'file') {
      onSelect(item);
    } else {
      setIsExpanded(!isExpanded);
    }
  };

  const isSelected = selectedFile?.id === item.id;

  return (
    <div>
      <div
        onClick={handleClick}
        className={`flex items-center px-2 py-1.5 cursor-pointer hover:bg-gray-100 transition-colors ${
          isSelected ? 'bg-blue-50 text-blue-700' : 'text-gray-700'
        }`}
        style={{ paddingLeft: `${level * 20 + 8}px` }}
      >
        {item.type === 'folder' && (
          <div className="mr-1">
            {isExpanded ? (
              <ChevronDown className="w-4 h-4" />
            ) : (
              <ChevronRight className="w-4 h-4" />
            )}
          </div>
        )}
        
        <div className="mr-2">
          {item.type === 'folder' ? (
            <Folder className="w-4 h-4" />
          ) : item.name.endsWith('.py') ? (
            <Python className="w-4 h-4 text-blue-600" />
          ) : (
            <File className="w-4 h-4" />
          )}
        </div>
        
        <span className="text-sm truncate">{item.name}</span>
      </div>
      
      {item.type === 'folder' && isExpanded && item.children && (
        <div>
          {item.children.map((child) => (
            <FileTreeItem
              key={child.id}
              item={child}
              level={level + 1}
              onSelect={onSelect}
              selectedFile={selectedFile}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export const FileSidebar: React.FC = () => {
  const { sidebarOpen, setSidebarOpen, currentFile, setCurrentFile } = useApp();
  const [files] = useState<FileItem[]>(mockFiles);

  const handleFileSelect = (file: FileItem) => {
    setCurrentFile(file);
  };

  if (!sidebarOpen) return null;

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-gray-900">Explorer</h3>
          <div className="flex items-center space-x-1">
            <button className="p-1 hover:bg-gray-100 rounded transition-colors">
              <Plus className="w-4 h-4 text-gray-600" />
            </button>
            <button className="p-1 hover:bg-gray-100 rounded transition-colors">
              <FolderPlus className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
        
        <div className="text-xs text-gray-500 font-medium uppercase tracking-wider">
          Python Project
        </div>
      </div>

      {/* File Tree */}
      <div className="flex-1 overflow-y-auto">
        {files.map((item) => (
          <FileTreeItem
            key={item.id}
            item={item}
            level={0}
            onSelect={handleFileSelect}
            selectedFile={currentFile}
          />
        ))}
      </div>
    </div>
  );
};