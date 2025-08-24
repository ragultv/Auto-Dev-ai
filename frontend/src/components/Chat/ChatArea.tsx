import React, { useState, useRef, useEffect } from 'react';
import { useApp } from '../../contexts/AppContext';
import { Send, Paperclip, ChevronDown } from 'lucide-react';
import { AIModel } from '../../types';

const models: { value: AIModel; label: string; color: string }[] = [
  { value: 'gpt-4', label: 'GPT-4', color: 'bg-green-500' },
  { value: 'claude-3', label: 'Claude 3', color: 'bg-orange-500' },
  { value: 'gemini-pro', label: 'Gemini Pro', color: 'bg-blue-500' }
];

export const ChatArea: React.FC = () => {
  const { 
    messages, 
    currentModel, 
    setCurrentModel, 
    addMessage,
    showPromptArea 
  } = useApp();
  
  const [inputValue, setInputValue] = useState('');
  const [showModelDropdown, setShowModelDropdown] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      addMessage(inputValue.trim(), 'user', currentModel);
      setInputValue('');
      
      // Simulate AI response
      setTimeout(() => {
        addMessage(`I understand you want to work with: "${inputValue.trim()}". Let me help you with that Python development task.`, 'ai', currentModel);
      }, 1000);
    }
  };

  const handleFileUpload = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      addMessage(`Uploaded file: ${file.name}`, 'user', currentModel);
    }
  };

  const selectedModel = models.find(m => m.value === currentModel) || models[0];

  if (showPromptArea) {
    return (
      <div className="h-screen flex items-center justify-center p-8 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-4xl w-full">
        
          <div className="text-center mb-12">
            <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl">
              <div className="w-12 h-12 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center">
                <div className="w-8 h-8 bg-white rounded-xl"></div>
              </div>
            </div>
            
            <h1 className="text-5xl font-bold text-gray-900 mb-4">AI Development Agent</h1>
            <p className="text-xl text-gray-600 mb-8">What would you like to build today?</p>
            <p className="text-sm text-gray-500">Describe your project and I'll help you create it step by step</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Describe your project... (e.g., 'Create a web scraper for news articles' or 'Build a machine learning model for sentiment analysis')"
                className="w-full p-8 pr-24 border-2 border-gray-200 rounded-3xl focus:border-blue-500 focus:ring-0 transition-all duration-200 resize-none text-lg shadow-lg"
                rows={6}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                    handleSubmit(e);
                  }
                }}
              />
              
              <div className="absolute bottom-6 right-6 flex items-center space-x-3">
                <button
                  type="button"
                  onClick={handleFileUpload}
                  className="p-3 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-xl transition-all duration-200"
                >
                  <Paperclip className="w-6 h-6" />
                </button>
                
                <button
                  type="submit"
                  disabled={!inputValue.trim()}
                  className="p-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                >
                  <Send className="w-6 h-6" />
                </button>
              </div>
            </div>

            <div className="text-center">
              <p className="text-sm text-gray-500">
                Press <kbd className="px-2 py-1 bg-gray-200 rounded text-xs">Ctrl+Enter</kbd> to send
              </p>
            </div>
          </form>

          <input
            ref={fileInputRef}
            type="file"
            onChange={handleFileChange}
            className="hidden"
            accept=".py,.txt,.md,.json,.yaml,.yml"
          />
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Chat Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
          <div className="relative">
            <button
              onClick={() => setShowModelDropdown(!showModelDropdown)}
              className="flex items-center space-x-2 px-3 py-1.5 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all duration-200"
            >
              <div className={`w-2 h-2 rounded-full ${selectedModel.color}`}></div>
              <span className="text-sm font-medium">{selectedModel.label}</span>
              <ChevronDown className="w-4 h-4 text-gray-400" />
            </button>

            {showModelDropdown && (
              <div className="absolute top-full right-0 mt-1 w-40 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                {models.map((model) => (
                  <button
                    key={model.value}
                    onClick={() => {
                      setCurrentModel(model.value);
                      setShowModelDropdown(false);
                    }}
                    className="w-full flex items-center space-x-2 px-4 py-2 hover:bg-gray-50 transition-colors first:rounded-t-lg last:rounded-b-lg"
                  >
                    <div className={`w-2 h-2 rounded-full ${model.color}`}></div>
                    <span className="text-sm">{model.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-4 rounded-2xl ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-gray-900 border border-gray-200'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              <div className="mt-2 flex items-center justify-between text-xs opacity-70">
                <span>{message.timestamp.toLocaleTimeString()}</span>
                {message.model && <span>{models.find(m => m.value === message.model)?.label}</span>}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        <form onSubmit={handleSubmit} className="flex items-end space-x-2">
          <div className="flex-1 relative">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type your message..."
              className="w-full p-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none"
              rows={1}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                  handleSubmit(e);
                }
              }}
            />
            
            <button
              type="button"
              onClick={handleFileUpload}
              className="absolute bottom-3 right-3 p-1 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <Paperclip className="w-4 h-4" />
            </button>
          </div>

          <button
            type="submit"
            disabled={!inputValue.trim()}
            className="p-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>

        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileChange}
          className="hidden"
          accept=".py,.txt,.md,.json,.yaml,.yml"
        />
      </div>
    </div>
  );
};