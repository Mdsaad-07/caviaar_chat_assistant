'use client';

import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, X, MessageCircle, Loader2, Bot, User, ExternalLink, Minimize2, Maximize2 } from 'lucide-react';
import { v4 as uuidv4 } from 'uuid';
import ReactMarkdown from 'react-markdown';

// Types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  suggestedProducts?: Product[];
}

interface Product {
  id: number;
  name: string;
  price: number;
  currency: string;
  image_url: string;
  url: string;
  category: string;
}

interface ChatResponse {
  response: string;
  session_id?: string;
  query_type?: string;
  tokens_used?: number;
  tokens_remaining?: number;
  suggested_products?: Product[];
}

const API_BASE_URL = 'http://localhost:8000';

// Custom components for ReactMarkdown - only render buttons for relevant links
const markdownComponents = {
  a: ({ node, children, href, ...props }: any) => {
    // Only render as button if it's a Caviaar Mode link
    if (href && (href.includes('caviaarmode.com') || href.startsWith('https://caviaarmode.com'))) {
      return (
        <a 
          {...props}
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block bg-black text-white px-4 py-2 rounded-full hover:bg-gray-800 transition-colors text-sm font-medium no-underline mx-1 my-1"
        >
          {children} <ExternalLink className="inline h-3 w-3 ml-1" />
        </a>
      );
    }
    // Regular link for other URLs
    return (
      <a {...props} href={href} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
        {children}
      </a>
    );
  },
  p: ({ children }: any) => <p className="mb-2 last:mb-0">{children}</p>
};

const CaviaarModeChat: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true); // Start open for demo
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "👋 Hi! I'm your Caviaar Mode assistant. I can help you with orders, returns, payments, and product questions. How can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setSessionId(uuidv4());
  }, []);

  useEffect(() => {
    if (isOpen && !isMinimized) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, isMinimized]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const endpoint = `${API_BASE_URL}/api/chat`;
      console.log('🔍 Sending request to:', endpoint);

      const response = await axios.post<ChatResponse>(endpoint, {
        query: userMessage.content,
        session_id: sessionId
      });

      console.log('✅ Response:', response.data);

      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(),
        suggestedProducts: response.data.suggested_products || []
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      if (response.data.session_id) {
        setSessionId(response.data.session_id);
      }

    } catch (error) {
      console.error('❌ Chat error:', error);
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: "I'm having trouble connecting right now. Please try again in a moment or contact support.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const quickSuggestions = [
    "Size guide",
    "Return policy", 
    "Payment methods",
    "Suggest shirts",
    "Current offers",
    "Shipping info"
  ];

  // Chat button (when closed)
  if (!isOpen) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsOpen(true)}
          className="bg-black hover:bg-gray-800 text-white rounded-full p-4 shadow-lg transform hover:scale-105 transition-all duration-200 flex items-center justify-center group"
          aria-label="Open chat"
        >
          <MessageCircle className="h-6 w-6" />
        </button>
      </div>
    );
  }

  // Main chat window
  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div 
        className={`bg-white rounded-2xl shadow-2xl border border-gray-200 transition-all duration-300 flex flex-col ${
          isMinimized 
            ? 'w-80 h-16' 
            : 'w-96 max-w-[calc(100vw-3rem)]'
        }`}
        style={{
          height: isMinimized ? '4rem' : 'min(600px, calc(100vh - 8rem))',
        }}
      >
        
        {/* Header */}
        <div className="bg-black text-white p-4 rounded-t-2xl flex items-center justify-between flex-shrink-0">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
              <span className="text-black font-bold text-sm">CM</span>
            </div>
            <div>
              <h3 className="font-medium text-sm">Caviaar Mode</h3>
              <p className="text-xs text-gray-300">AI Assistant</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="text-white hover:text-gray-300 transition-colors"
            >
              {isMinimized ? <Maximize2 className="h-4 w-4" /> : <Minimize2 className="h-4 w-4" />}
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-300 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {!isMinimized && (
          <>
            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 min-h-0">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex items-start space-x-2 max-w-[85%] ${
                    message.role === 'user' ? 'flex-row-reverse space-x-reverse' : 'flex-row'
                  }`}>
                    {/* Avatar */}
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.role === 'user' 
                        ? 'bg-black text-white' 
                        : 'bg-gray-200 text-gray-600'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="h-4 w-4" />
                      ) : (
                        <Bot className="h-4 w-4" />
                      )}
                    </div>

                    {/* Message Bubble */}
                    <div className="flex-1">
                      <div className={`rounded-2xl px-4 py-2 ${
                        message.role === 'user'
                          ? 'bg-black text-white'
                          : 'bg-white text-gray-800 border border-gray-200 shadow-sm'
                      }`}>
                        {message.role === 'assistant' ? (
                          <ReactMarkdown 
                            className="text-sm prose prose-sm max-w-none"
                            components={markdownComponents}
                          >
                            {message.content}
                          </ReactMarkdown>
                        ) : (
                          <p className="text-sm">{message.content}</p>
                        )}
                      </div>

                      <p className="text-xs mt-1 opacity-70 text-gray-500">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </div>
                </div>
              ))}

              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="flex items-start space-x-2">
                    <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                      <Bot className="h-4 w-4 text-gray-600" />
                    </div>
                    <div className="bg-white rounded-2xl px-4 py-2 border border-gray-200 shadow-sm">
                      <div className="flex items-center space-x-2">
                        <Loader2 className="h-4 w-4 animate-spin text-gray-500" />
                        <span className="text-sm text-gray-600">Typing...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Suggestions */}
            <div className="px-4 py-2 border-t border-gray-200 bg-white flex-shrink-0">
              <div className="flex flex-wrap gap-2">
                {quickSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => setInput(suggestion)}
                    className="text-xs px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors duration-200 border"
                    disabled={isLoading}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>

            {/* Input Form */}
            <div className="p-4 border-t border-gray-200 bg-white rounded-b-2xl flex-shrink-0">
              <form onSubmit={sendMessage} className="flex space-x-3 mb-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:ring-2 focus:ring-black focus:border-transparent outline-none text-sm"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={!input.trim() || isLoading}
                  className="bg-black hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-full p-2 transition-colors duration-200 flex-shrink-0"
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </button>
              </form>

              {/* Footer */}
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Powered by Caviaar Mode AI</span>
                <a 
                  href="https://caviaarmode.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-black hover:underline flex items-center"
                >
                  Visit Store <ExternalLink className="h-3 w-3 ml-1" />
                </a>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CaviaarModeChat;
