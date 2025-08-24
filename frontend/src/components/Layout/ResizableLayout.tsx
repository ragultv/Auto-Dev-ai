import React, { useState, useCallback } from 'react';
import { useApp } from '../../contexts/AppContext';
import { ChatArea } from '../Chat/ChatArea';
import { EditorArea } from '../Editor/EditorArea';

export const ResizableLayout: React.FC = () => {
  const { chatWidth, setChatWidth } = useApp();
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseDown = useCallback(() => {
    setIsDragging(true);
  }, []);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isDragging) return;
    
    const newWidth = (e.clientX / window.innerWidth) * 100;
    const clampedWidth = Math.max(20, Math.min(50, newWidth));
    setChatWidth(clampedWidth);
  }, [isDragging, setChatWidth]);

  React.useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    } else {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isDragging, handleMouseMove, handleMouseUp]);

  return (
    <div className="h-screen flex">
      {/* Chat Area */}
      <div 
        className="border-r border-gray-200"
        style={{ width: `${chatWidth}%` }}
      >
        <ChatArea />
      </div>

      {/* Resize Handle */}
      <div
        onMouseDown={handleMouseDown}
        className={`w-1 bg-gray-200 hover:bg-blue-500 cursor-col-resize transition-colors duration-200 ${
          isDragging ? 'bg-blue-500' : ''
        }`}
      />

      {/* Editor Area */}
      <div 
        className="flex-1"
        style={{ width: `${100 - chatWidth}%` }}
      >
        <EditorArea />
      </div>
    </div>
  );
};