import React from 'react';
import { Menu, Bot, Wifi, WifiOff } from 'lucide-react';

export default function Header({ onToggleSidebar, isOnline = true }) {
  return (
    <header className="app-header">
      <div className="header-left">
        <button
          className="mobile-menu-btn"
          onClick={onToggleSidebar}
          aria-label="Open sidebar menu"
          title="Open menu"
        >
          <Menu size={22} />
        </button>

        <div className="header-branding">
          <div className="header-title-row">
            <h1 className="header-title">Amazon Help AI</h1>
          </div>
          <span className="header-subtitle">AI-powered customer support</span>
        </div>
      </div>

      <div className="header-right">
        <div className={`agent-status-badge ${isOnline ? '' : 'offline'}`}>
          <span className={`status-dot ${isOnline ? 'pulsing' : ''}`}></span>
          <span>{isOnline ? 'AI Agent Online' : 'Agent Offline'}</span>
        </div>
      </div>
    </header>
  );
}
