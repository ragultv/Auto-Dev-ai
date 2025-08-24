import React, { useState, useRef, useEffect } from 'react';
import { Terminal, Play, Square, RotateCcw } from 'lucide-react';

interface TerminalLine {
  id: string;
  text: string;
  type: 'input' | 'output' | 'error';
  timestamp: Date;
}

export const TerminalPanel: React.FC = () => {
  const [lines, setLines] = useState<TerminalLine[]>([
    {
      id: '1',
      text: 'Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32',
      type: 'output',
      timestamp: new Date()
    },
    {
      id: '2',
      text: 'Type "help", "copyright", "credits" or "license" for more information.',
      type: 'output',
      timestamp: new Date()
    }
  ]);
  
  const [inputValue, setInputValue] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const terminalEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [lines]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isRunning) {
      const command = inputValue.trim();
      
      // Add input line
      const inputLine: TerminalLine = {
        id: Date.now().toString(),
        text: `>>> ${command}`,
        type: 'input',
        timestamp: new Date()
      };
      
      setLines(prev => [...prev, inputLine]);
      setInputValue('');
      setIsRunning(true);

      // Simulate command execution
      setTimeout(() => {
        const outputLine: TerminalLine = {
          id: (Date.now() + 1).toString(),
          text: simulateCommand(command),
          type: command.includes('error') ? 'error' : 'output',
          timestamp: new Date()
        };
        
        setLines(prev => [...prev, outputLine]);
        setIsRunning(false);
      }, 1000 + Math.random() * 2000);
    }
  };

  const simulateCommand = (command: string): string => {
    if (command.includes('print')) {
      return command.replace(/print\(['"](.+?)['"]\)/, '$1');
    }
    
    if (command.includes('error')) {
      return 'Traceback (most recent call last):\n  File "<stdin>", line 1, in <module>\nNameError: name \'error\' is not defined';
    }
    
    if (command.includes('help')) {
      return 'Type help() for interactive help, or help(object) for help about object.';
    }
    
    if (command.includes('import')) {
      return '';
    }
    
    if (command.includes('=')) {
      return '';
    }
    
    return `Executed: ${command}`;
  };

  const handleClear = () => {
    setLines([]);
  };

  const handleStop = () => {
    setIsRunning(false);
    const stopLine: TerminalLine = {
      id: Date.now().toString(),
      text: 'KeyboardInterrupt',
      type: 'error',
      timestamp: new Date()
    };
    setLines(prev => [...prev, stopLine]);
  };

  return (
    <div className="h-full bg-gray-900 text-white flex flex-col">
      {/* Terminal Header */}
      <div className="bg-gray-800 px-4 py-2 flex items-center justify-between border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <Terminal className="w-4 h-4" />
          <span className="text-sm font-medium">Python Terminal</span>
        </div>
        
        <div className="flex items-center space-x-2">
          {isRunning ? (
            <button
              onClick={handleStop}
              className="p-1.5 hover:bg-gray-700 rounded transition-colors"
              title="Stop execution"
            >
              <Square className="w-4 h-4 text-red-400" />
            </button>
          ) : (
            <button
              onClick={() => {
                if (inputValue.trim()) {
                  const form = new Event('submit');
                  handleSubmit(form as any);
                }
              }}
              className="p-1.5 hover:bg-gray-700 rounded transition-colors"
              title="Run current input"
            >
              <Play className="w-4 h-4 text-green-400" />
            </button>
          )}
          
          <button
            onClick={handleClear}
            className="p-1.5 hover:bg-gray-700 rounded transition-colors"
            title="Clear terminal"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Terminal Output */}
      <div className="flex-1 overflow-y-auto p-4 font-mono text-sm">
        {lines.map((line) => (
          <div
            key={line.id}
            className={`mb-1 ${
              line.type === 'error'
                ? 'text-red-400'
                : line.type === 'input'
                ? 'text-green-400'
                : 'text-gray-300'
            }`}
          >
            <pre className="whitespace-pre-wrap">{line.text}</pre>
          </div>
        ))}
        
        {isRunning && (
          <div className="text-yellow-400 animate-pulse">
            Executing...
          </div>
        )}
        
        <div ref={terminalEndRef} />
      </div>

      {/* Terminal Input */}
      <div className="bg-gray-800 p-4 border-t border-gray-700">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <span className="text-green-400 font-mono">{'>>>'}</span>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Enter Python code..."
            disabled={isRunning}
            className="flex-1 bg-transparent text-white placeholder-gray-500 outline-none font-mono disabled:opacity-50"
          />
        </form>
      </div>
    </div>
  );
};