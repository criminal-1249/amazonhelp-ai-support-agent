import React, { useState, useEffect, useCallback, useRef } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import { sendChatMessage, checkBackendHealth } from './services/api';
import {
  loadConversations,
  saveConversations,
  getActiveConversationId,
  setActiveConversationId,
} from './utils/storage';
import './App.css';

export default function App() {
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isOnline, setIsOnline] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const lastSuccessRef = useRef(Date.now());
  const checkSeqRef = useRef(0);

  // Initialize conversations from localStorage on initial load
  useEffect(() => {
    const saved = loadConversations();
    setConversations(saved);

    const savedActiveId = getActiveConversationId();
    if (savedActiveId && saved.some((c) => c.id === savedActiveId)) {
      const activeConv = saved.find((c) => c.id === savedActiveId);
      setActiveId(savedActiveId);
      setMessages(activeConv.messages || []);
    }
  }, []);

  // Health check on mount and periodic polling with race-condition guards
  const runHealthCheck = useCallback(async () => {
    const seq = ++checkSeqRef.current;
    const res = await checkBackendHealth();

    // Prevent race condition: ignore if a newer health check was fired
    if (seq !== checkSeqRef.current) return;

    // If chat or health check recently succeeded (within 15s), avoid false offline flutter
    if (!res.ok && Date.now() - lastSuccessRef.current < 15000) {
      return;
    }

    setIsOnline(res.ok);
    if (res.ok) {
      lastSuccessRef.current = Date.now();
    }
  }, []);

  useEffect(() => {
    let isMounted = true;
    let timerId = null;

    const scheduleNext = () => {
      if (!isMounted) return;
      timerId = setTimeout(async () => {
        await runHealthCheck();
        scheduleNext();
      }, 25000);
    };

    // Execute immediately on application load
    runHealthCheck().then(scheduleNext);

    return () => {
      isMounted = false;
      if (timerId) clearTimeout(timerId);
    };
  }, [runHealthCheck]);

  // Handler: Start a new conversation thread
  const handleNewConversation = () => {
    setActiveId(null);
    setMessages([]);
    setError(null);
    setActiveConversationId(null);
    setSidebarOpen(false);
  };

  // Handler: Select an existing conversation
  const handleSelectConversation = (id) => {
    const found = conversations.find((c) => c.id === id);
    if (found) {
      setActiveId(id);
      setMessages(found.messages || []);
      setError(null);
      setActiveConversationId(id);
      setSidebarOpen(false);
    }
  };

  // Handler: Delete a conversation
  const handleDeleteConversation = (id) => {
    const updated = conversations.filter((c) => c.id !== id);
    setConversations(updated);
    saveConversations(updated);

    if (activeId === id) {
      if (updated.length > 0) {
        setActiveId(updated[0].id);
        setMessages(updated[0].messages || []);
        setActiveConversationId(updated[0].id);
      } else {
        handleNewConversation();
      }
    }
  };

  // Handler: Send a chat message
  const handleSendMessage = async (text) => {
    if (!text || !text.trim() || isLoading) return;

    setError(null);

    // Customer message object
    const userMessage = {
      id: `user-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
      role: 'customer',
      text: text.trim(),
      timestamp: new Date().toISOString(),
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      // Call backend API
      const result = await sendChatMessage(text);

      const aiMessage = {
        id: `ai-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
        role: 'assistant',
        text: result.response,
        response: result.response,
        intent: result.intent,
        decision: result.decision,
        reason: result.reason,
        evidence: result.evidence || [],
        timestamp: new Date().toISOString(),
      };

      const finalMessages = [...newMessages, aiMessage];
      setMessages(finalMessages);

      // Save / Update conversation in localStorage
      let currentId = activeId;
      let updatedConversations;

      if (!currentId) {
        // Create new conversation entry
        currentId = `conv-${Date.now()}`;
        setActiveId(currentId);
        setActiveConversationId(currentId);

        const newConv = {
          id: currentId,
          title: text.length > 38 ? `${text.substring(0, 38)}...` : text,
          updatedAt: Date.now(),
          messages: finalMessages,
        };

        updatedConversations = [newConv, ...conversations];
      } else {
        // Update existing conversation entry
        updatedConversations = conversations.map((conv) => {
          if (conv.id === currentId) {
            return {
              ...conv,
              updatedAt: Date.now(),
              messages: finalMessages,
            };
          }
          return conv;
        });
      }

      setConversations(updatedConversations);
      saveConversations(updatedConversations);
      lastSuccessRef.current = Date.now();
      setIsOnline(true);
    } catch (err) {
      console.error('API Error:', err);
      const errorMessage =
        err.message ||
        "Sorry, I'm having trouble connecting to the support agent. Please try again.";
      setError(errorMessage);

      // Also create an informative error message bubble so it stays visible in conversation
      const errorAiMessage = {
        id: `ai-err-${Date.now()}`,
        role: 'assistant',
        text: errorMessage,
        response: errorMessage,
        decision: 'ESCALATE',
        reason: 'Network or backend connectivity error occurred while communicating with the agent server.',
        evidence: [],
        timestamp: new Date().toISOString(),
      };

      const finalWithErr = [...newMessages, errorAiMessage];
      setMessages(finalWithErr);
      setIsOnline(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Left Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        conversations={conversations}
        activeId={activeId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        onDeleteConversation={handleDeleteConversation}
      />

      {/* Main Chat Area */}
      <div className="main-wrapper">
        <Header
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          isOnline={isOnline}
        />

        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}
          onSelectPrompt={handleSendMessage}
        />

        <MessageInput
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
