import React from 'react';
import { useApp } from '../../contexts/AppContext';
import { Eye, ExternalLink } from 'lucide-react';

export const PreviewPanel: React.FC = () => {
  const { currentFile } = useApp();

  const renderPreview = () => {
    if (!currentFile) {
      return (
        <div className="h-full flex items-center justify-center text-gray-500">
          <div className="text-center">
            <Eye className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium mb-2">No preview available</p>
            <p className="text-sm">Select a Python file to see its preview</p>
          </div>
        </div>
      );
    }

    if (!currentFile.name.endsWith('.py')) {
      return (
        <div className="h-full flex items-center justify-center text-gray-500">
          <div className="text-center">
            <Eye className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium mb-2">Preview not available</p>
            <p className="text-sm">This file type cannot be previewed</p>
          </div>
        </div>
      );
    }

    return (
      <div className="h-full p-6">
        <div className="bg-white rounded-lg border border-gray-200 h-full overflow-y-auto">
          {/* Preview Header */}
          <div className="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Eye className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-900">{currentFile.name}</span>
            </div>
            <button className="p-1 hover:bg-gray-200 rounded transition-colors">
              <ExternalLink className="w-4 h-4 text-gray-600" />
            </button>
          </div>

          {/* Code Analysis */}
          <div className="p-4 space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">File Analysis</h3>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p className="text-sm text-blue-800">
                  This Python file contains {currentFile.content?.split('\n').length || 0} lines of code.
                </p>
              </div>
            </div>

            {/* Function Detection */}
            {currentFile.content?.includes('def ') && (
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-2">Functions</h3>
                <div className="space-y-2">
                  {currentFile.content
                    .split('\n')
                    .filter(line => line.trim().startsWith('def '))
                    .map((line, index) => {
                      const funcName = line.trim().split('(')[0].replace('def ', '');
                      return (
                        <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-2">
                          <code className="text-sm text-green-800 font-mono">{funcName}()</code>
                        </div>
                      );
                    })}
                </div>
              </div>
            )}

            {/* Import Detection */}
            {(currentFile.content?.includes('import ') || currentFile.content?.includes('from ')) && (
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-2">Imports</h3>
                <div className="space-y-2">
                  {currentFile.content
                    .split('\n')
                    .filter(line => line.trim().startsWith('import ') || line.trim().startsWith('from '))
                    .map((line, index) => (
                      <div key={index} className="bg-purple-50 border border-purple-200 rounded-lg p-2">
                        <code className="text-sm text-purple-800 font-mono">{line.trim()}</code>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* Docstring Detection */}
            {currentFile.content?.includes('"""') && (
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-2">Documentation</h3>
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-3">
                  <p className="text-sm text-orange-800">
                    This file contains docstrings and documentation.
                  </p>
                </div>
              </div>
            )}

            {/* Code Quality Indicators */}
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-2">Code Quality</h3>
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-green-50 border border-green-200 rounded-lg p-2 text-center">
                  <div className="text-lg font-bold text-green-700">
                    {currentFile.content?.includes('"""') ? '✓' : '✗'}
                  </div>
                  <div className="text-xs text-green-600">Documented</div>
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-2 text-center">
                  <div className="text-lg font-bold text-blue-700">
                    {(currentFile.content?.split('\n').length || 0) < 100 ? '✓' : '!'}
                  </div>
                  <div className="text-xs text-blue-600">Size</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="h-full bg-gray-50">
      {renderPreview()}
    </div>
  );
};