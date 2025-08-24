import React, { useRef } from 'react';
import Editor from '@monaco-editor/react';
import { useApp } from '../../contexts/AppContext';

export const MonacoEditor: React.FC = () => {
  const { currentFile, setCurrentFile } = useApp();
  const editorRef = useRef(null);

  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor;
  };

  const handleEditorChange = (value: string | undefined) => {
    if (currentFile && value !== undefined) {
      setCurrentFile({
        ...currentFile,
        content: value
      });
    }
  };

  return (
    <div className="h-full">
      {currentFile ? (
        <Editor
          height="100%"
          defaultLanguage="python"
          value={currentFile.content}
          onChange={handleEditorChange}
          onMount={handleEditorDidMount}
          theme="vs-light"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            roundedSelection: false,
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            insertSpaces: true,
            wordWrap: 'on',
            bracketPairColorization: { enabled: true },
            suggest: {
              showKeywords: true,
              showSnippets: true,
            },
          }}
        />
      ) : (
        <div className="h-full flex items-center justify-center text-gray-500">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 opacity-50">
              <svg viewBox="0 0 24 24" className="w-full h-full">
                <path
                  fill="currentColor"
                  d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"
                />
              </svg>
            </div>
            <p className="text-lg font-medium mb-2">No file selected</p>
            <p className="text-sm">Select a file from the explorer to start editing</p>
          </div>
        </div>
      )}
    </div>
  );
};