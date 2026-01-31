import React, { useState, useEffect, useRef } from 'react';
import Head from 'next/head';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface POI {
  poiId: string;
  name: string;
  category?: string;
  duration?: number;
  arrivalTime?: string;
  departureTime?: string;
}

interface Block {
  type: string;
  pois: POI[];
  travelTime?: number;
  totalDuration?: number;
  time?: {
    start: string;
    end: string;
  };
}

interface Day {
  day: number;
  date?: string;
  blocks: Block[];
  totalTravelTime?: number;
  feasibilityScore?: number;
}

interface Itinerary {
  days: Day[];
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: '👋 Hi! I\'m your AI travel planner. Tell me about your dream trip! For example: "Plan a 3-day trip to Jaipur. I like food and culture, relaxed pace."',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [email1, setEmail1] = useState('');
  const [isSendingEmail, setIsSendingEmail] = useState(false);
  const [emailSuccess, setEmailSuccess] = useState<string | null>(null);
  // Hardcoded emails as per requirement
  const SENDER_EMAIL = "ashup2707@gmail.com";
  const RECEIVER_EMAIL = "f20201480g@alumni.bits-pilani.ac.in";
  const [sources, setSources] = useState<Array<{source: string, type: string}>>([]);
  const [ragCitations, setRagCitations] = useState<Array<any>>([]);
  const [ragDescriptions, setRagDescriptions] = useState<Record<string, string>>({});
  const [backendReady, setBackendReady] = useState<boolean | null>(null);
  const [llmConfigured, setLlmConfigured] = useState<boolean | null>(null);

  // Check backend readiness (for Loom / demo)
  useEffect(() => {
    let cancelled = false;
    const check = async () => {
      try {
        const res = await fetch(`${API_URL}/health/ready`);
        if (cancelled) return;
        const data = await res.json().catch(() => ({}));
        setBackendReady(res.ok);
        setLlmConfigured(!!data?.llm_configured);
      } catch {
        if (!cancelled) setBackendReady(false);
      }
    };
    check();
    const t = setInterval(check, 15000);
    return () => { cancelled = true; clearInterval(t); };
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = false;
        recognitionRef.current.lang = 'en-US';

        recognitionRef.current.onstart = () => {
          console.log('Voice recognition started');
          setIsListening(true);
        };

        recognitionRef.current.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          console.log('Transcript:', transcript);
          setInputText(transcript);
        };

        recognitionRef.current.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error);
          setIsListening(false);
          setError(`Voice error: ${event.error}. Make sure microphone access is allowed.`);
          setTimeout(() => setError(null), 3000);
        };

        recognitionRef.current.onend = () => {
          console.log('Voice recognition ended');
          setIsListening(false);
        };
      } else {
        console.warn('Speech recognition not supported in this browser');
      }
    }
  }, []);

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      setError('Voice recognition not supported in this browser. Please use Chrome or Edge.');
      setTimeout(() => setError(null), 3000);
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
    } else {
      try {
        recognitionRef.current.start();
      } catch (err) {
        console.error('Failed to start voice recognition:', err);
        setError('Failed to start voice recognition. Please try again.');
        setTimeout(() => setError(null), 3000);
      }
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: inputText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setError(null);

    try {
      console.log('Sending to backend:', inputText);
      console.log('API URL:', API_URL);

      // Detect if it's an edit command
      const lowerInput = inputText.toLowerCase();
      const isEdit = itinerary && (
        lowerInput.includes('make day') ||
        lowerInput.includes('swap') ||
        lowerInput.includes('reduce') ||
        lowerInput.includes('add ') ||
        lowerInput.includes('remove') ||
        lowerInput.includes('change day') ||
        /day\s*\d+/.test(lowerInput) ||
        /day\s*(one|two|three|four|five)/.test(lowerInput)
      );

      // Detect if it's a question (explain: why, doable, rain/weather)
      const isQuestion = itinerary && (
        lowerInput.includes('why') ||
        lowerInput.includes('what if') ||
        lowerInput.includes('doable') ||
        lowerInput.includes('feasible') ||
        lowerInput.includes('realistic') ||
        lowerInput.includes('rain') ||
        lowerInput.includes('weather') ||
        lowerInput.includes('is this plan')
      );

      let endpoint = '/api/plan';
      let body: any = { user_input: inputText };

      if (isEdit) {
        endpoint = '/api/edit';
        body = { edit_command: inputText };
      } else if (isQuestion) {
        endpoint = '/api/explain';
        body = { question: inputText };
      }

      console.log('Endpoint:', endpoint);
      console.log('Request body:', body);

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      console.log('Response status:', response.status);

      const result = await response.json();
      console.log('Backend response:', result);

      let assistantMessage: Message;

      if (result.action === 'ask') {
        assistantMessage = {
          role: 'assistant',
          content: result.message,
          timestamp: new Date()
        };
      } else if (result.action === 'itinerary') {
        setItinerary(result.itinerary);
        
        // Store RAG data if available
        if (result.rag_citations) {
          setRagCitations(result.rag_citations);
        }
        if (result.rag_descriptions) {
          setRagDescriptions(result.rag_descriptions);
        }
        
        const ragInfo = result.rag_loaded ? `\n\n📚 Enriched with travel guide information from ${result.rag_citations?.length || 0} sources` : '';
        assistantMessage = {
          role: 'assistant',
          content: `✅ ${result.message}\n\nI've created a ${result.itinerary.days.length}-day itinerary with ${result.poi_count} places to visit. Check it out on the right! 👉${ragInfo}`,
          timestamp: new Date()
        };
      } else if (result.action === 'edit_applied') {
        setItinerary(result.itinerary);
        assistantMessage = {
          role: 'assistant',
          content: `✅ ${result.message}\n\nYour itinerary has been updated! ${result.changes.length} changes made.`,
          timestamp: new Date()
        };
      } else if (result.answer) {
        assistantMessage = {
          role: 'assistant',
          content: result.answer + (result.citations?.length > 0 ? `\n\n📚 Sources: ${result.citations.map((c: any) => c.source).join(', ')}` : ''),
          timestamp: new Date()
        };
      } else if (result.explanation) {
        assistantMessage = {
          role: 'assistant',
          content: result.explanation + (result.citations?.length > 0 ? `\n\n📚 Sources: ${result.citations.map((c: any) => c.source).join(', ')}` : ''),
          timestamp: new Date()
        };
      } else if (result.action === 'error') {
        assistantMessage = {
          role: 'assistant',
          content: `❌ ${result.message}`,
          timestamp: new Date()
        };
      } else {
        assistantMessage = {
          role: 'assistant',
          content: 'Something went wrong. Please try again.',
          timestamp: new Date()
        };
      }

      setMessages(prev => [...prev, assistantMessage]);

      // Extract and store sources/citations
      if (result.citations && result.citations.length > 0) {
        const newSources = result.citations.map((citation: any) => ({
          source: citation.source || citation,
          type: citation.type || 'general'
        }));
        setSources(prev => {
          // Avoid duplicates
          const existingSources = prev.map(s => s.source);
          const uniqueNew = newSources.filter((s: any) => !existingSources.includes(s.source));
          return [...prev, ...uniqueNew];
        });
      }

      // Text-to-speech for assistant response
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(assistantMessage.content.replace(/[👋✅❌📚👉]/g, ''));
        utterance.rate = 1;
        speechSynthesis.speak(utterance);
      }

    } catch (err) {
      console.error('Connection error:', err);
      setError('Failed to connect to server. Make sure backend is running on http://localhost:8000');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Failed to connect to backend server. Please ensure:\n1. Backend is running: cd backend && python3 main.py\n2. Backend is on http://localhost:8000\n3. Check the browser console for details',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (isoTime: string) => {
    const date = new Date(isoTime);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
  };

  const getBlockIcon = (type: string) => {
    switch (type) {
      case 'morning': return '🌅';
      case 'afternoon': return '☀️';
      case 'evening': return '🌆';
      default: return '📍';
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSendEmail = async () => {
    const toEmail = email1.trim() || RECEIVER_EMAIL;
    const emailsToSend = [toEmail];

    setIsSendingEmail(true);
    setError(null);
    setEmailSuccess(null);

    try {
      const response = await fetch(`${API_URL}/api/send-email`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipient_emails: emailsToSend,
          subject: 'Your Travel Itinerary from Voyage'
        })
      });

      const result = await response.json().catch(() => ({}));
      const detail = typeof result.detail === 'string' ? result.detail : result.message || 'Failed to send email';

      if (response.ok && result.success) {
        setEmailSuccess(`✅ Itinerary PDF sent to ${emailsToSend.join(', ')}`);
        setTimeout(() => {
          setEmailSuccess(null);
          setShowEmailModal(false);
        }, 3000);
      } else {
        let errorMsg = detail;
        if (response.status === 503) {
          errorMsg = 'Email is not configured. Add SENDER_PASSWORD (Gmail App Password) to backend .env and restart the backend.';
        } else if (result.error === 'authentication_failed') {
          errorMsg = result.message || 'Gmail login failed. Use an App Password in .env (see Google Account → Security → App passwords).';
        } else if (result.error === 'connection_error') {
          errorMsg = result.message || 'Could not reach email server. Check network and try again.';
        }
        setError(errorMsg);
        setTimeout(() => setError(null), 10000);
      }
    } catch (err: any) {
      console.error('Email error:', err);
      setError(err?.message || 'Could not reach backend. Ensure the backend is running and CORS is allowed.');
      setTimeout(() => setError(null), 10000);
    } finally {
      setIsSendingEmail(false);
    }
  };

  const handleCloseEmailModal = () => {
    setShowEmailModal(false);
    setError(null);
    setEmailSuccess(null);
  };

  return (
    <>
      <Head>
        <title>Voyage - AI Travel Planner</title>
        <meta name="description" content="Voice-first AI travel planning assistant" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Pacifico&display=swap" rel="stylesheet" />
      </Head>

      <div className="app-container">
        {/* Left Panel - Chat Interface */}
        <div className="chat-panel">
          <div className="chat-header">
            <div className="logo">
              <span className="logo-icon">✈️</span>
              <h1 className="logo-text">Voyage</h1>
            </div>
            <p className="tagline">AI travel planning assistant</p>
            {backendReady === true && (
              <div className="status-row">
                <span className="status-badge connected">● Backend connected</span>
                {llmConfigured === false && (
                  <span className="status-badge warning">Add GROQ_API_KEY or GEMINI_API_KEY to .env for planning</span>
                )}
              </div>
            )}
          </div>

          <div className="messages-container">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-text">{msg.content}</div>
                  <div className="message-time">
                    {msg.timestamp.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className="error-banner">
              ⚠️ {error}
            </div>
          )}

          <div className="input-container">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isListening ? 'Listening…' : 'Type or click mic to speak…'}
              disabled={isLoading}
              className="chat-input"
            />
            <button
              onClick={toggleVoiceInput}
              className={`voice-button ${isListening ? 'listening' : ''}`}
              disabled={isLoading}
              title={isListening ? 'Stop recording' : 'Click to speak'}
            >
              {isListening ? '⏹️' : '🎤'}
            </button>
            <button
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
              className="send-button"
            >
              ➤
            </button>
          </div>
        </div>

        {/* Middle Panel - Itinerary */}
        <div className="itinerary-panel">
          {itinerary ? (
          <>
            <div className="itinerary-header">
              <h2 className="itinerary-main-title">Itinerary</h2>
              <div className="itinerary-title-row">
                <div className="itinerary-stats">
                  <div className="stat-badge">
                    <span className="stat-icon">📅</span>
                    <span>{itinerary.days.length} Days</span>
                  </div>
                  <div className="stat-badge">
                    <span className="stat-icon">📍</span>
                    <span>{itinerary.days.reduce((sum, day) => 
                      sum + day.blocks.reduce((blockSum, block) => blockSum + block.pois.length, 0), 0
                    )} Places</span>
                  </div>
                </div>
                <button 
                  className="email-button-new"
                  onClick={() => setShowEmailModal(true)}
                  title="Send itinerary via email"
                >
                  <span className="email-icon">📧</span>
                  <span>Share</span>
                </button>
              </div>
            </div>

            <div className="itinerary-content">
              {itinerary.days.map((day, dayIdx) => (
                <div key={dayIdx} className="day-card">
                  <div className="day-header">
                    <div className="day-title">
                      <span className="day-badge">Day {day.day}</span>
                      {day.date && <span className="day-date">📅 {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>}
                    </div>
                    {day.feasibilityScore !== undefined && (
                      <div className="feasibility-badge-new" style={{
                        background: day.feasibilityScore >= 0.8 ? '#4caf50' : day.feasibilityScore >= 0.6 ? '#ff9800' : '#f44336'
                      }}>
                        <span className="badge-icon">✓</span>
                        <span>{(day.feasibilityScore * 100).toFixed(0)}%</span>
                      </div>
                    )}
                  </div>

                  <div className="day-blocks">
                    {day.blocks.map((block, blockIdx) => (
                      block.pois.length > 0 && (
                        <div key={blockIdx} className={`time-block ${block.type}`}>
                          <div className="block-header">
                            <span className="block-icon">{getBlockIcon(block.type)}</span>
                            <span className="block-time">
                              {block.type.charAt(0).toUpperCase() + block.type.slice(1)}
                              {block.time && ` • ${formatTime(block.time.start)} - ${formatTime(block.time.end)}`}
                            </span>
                          </div>
                          <div className="block-pois">
                            {block.pois.map((poi, poiIdx) => (
                              <div key={poiIdx} className="poi-item">
                                <div className="poi-name">
                                  <span className="poi-bullet">•</span>
                                  {poi.name || 'Unknown Location'}
                                </div>
                                {poi.duration && (
                                  <div className="poi-duration">
                                    🕐 {poi.duration} min
                                  </div>
                                )}
                                {ragDescriptions[poi.poiId] && (
                                  <div className="poi-rag-description">
                                    📖 {ragDescriptions[poi.poiId]}
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                          {block.travelTime !== undefined && block.travelTime > 0 && (
                            <div className="travel-info">
                              🚗 {block.travelTime} min travel time
                            </div>
                          )}
                        </div>
                      )
                    ))}
                  </div>

                  {day.totalTravelTime !== undefined && day.totalTravelTime > 0 && (
                    <div className="day-footer">
                      <span className="footer-icon">🚗</span>
                      Total Travel Time: {day.totalTravelTime} minutes
                    </div>
                  )}
                </div>
              ))}
            </div>
          </>
          ) : (
            <div className="itinerary-placeholder">
              <h3 className="placeholder-title">No itinerary yet</h3>
              <p className="placeholder-subtitle">Start planning from the chat.</p>
            </div>
          )}
        </div>

        {/* Right Panel - Sources */}
        <div className="sources-panel">
          {(sources.length > 0 || ragCitations.length > 0) ? (
            <div className="sources-section">
              <div className="sources-header">
                <h3>Sources</h3>
                <span className="sources-count">{sources.length + ragCitations.length}</span>
              </div>
              <div className="sources-content">
                {sources.map((source, idx) => (
                  <div key={idx} className="source-card">
                    <div className="source-icon">
                      {source.source.toLowerCase().includes('wikipedia') ? '📖' :
                       source.source.toLowerCase().includes('wikivoyage') ? '🗺️' :
                       source.source.toLowerCase().includes('osm') || source.source.toLowerCase().includes('openstreet') ? '📍' :
                       '🔗'}
                    </div>
                    <div className="source-text">{source.source}</div>
                  </div>
                ))}
                {ragCitations.map((citation, idx) => (
                  <div key={`rag-${idx}`} className="source-card">
                    <div className="source-icon">
                      {citation.source?.toLowerCase().includes('wikipedia') ? '📖' :
                       citation.source?.toLowerCase().includes('wikivoyage') ? '🗺️' :
                       citation.source?.toLowerCase().includes('rajasthan') ? '🏛️' :
                       citation.source?.toLowerCase().includes('tripadvisor') ? '⭐' :
                       '🔗'}
                    </div>
                    <div className="source-text">
                      <div className="source-name">{citation.source || 'Travel Guide'}</div>
                      {citation.poi && <div className="source-poi">📍 {citation.poi}</div>}
                      {citation.section && <div className="source-section">📑 {citation.section}</div>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="sources-empty">
              <h3>Sources</h3>
              <p>No sources yet.</p>
            </div>
          )}
        </div>

        {/* Email Modal */}
        {showEmailModal && (
          <div className="modal-overlay" onClick={handleCloseEmailModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h3>📧 Send Itinerary via Email</h3>
                <button className="modal-close" onClick={handleCloseEmailModal}>×</button>
              </div>
              <div className="modal-body">
                <p className="modal-description">
                  Send your itinerary as a PDF. Optional: enter a different recipient below (default: {RECEIVER_EMAIL}).
                </p>
                <div className="email-info">
                  <div className="email-info-row">
                    <strong>From:</strong> {SENDER_EMAIL}
                  </div>
                  <div className="email-input-row">
                    <label htmlFor="email-to">To (optional):</label>
                    <input
                      id="email-to"
                      type="email"
                      placeholder={RECEIVER_EMAIL}
                      value={email1}
                      onChange={(e) => setEmail1(e.target.value)}
                      className="email-input"
                    />
                  </div>
                  {!email1.trim() && (
                    <div className="email-info-row email-default">
                      <strong>Default To:</strong> {RECEIVER_EMAIL}
                    </div>
                  )}
                </div>
                {emailSuccess && (
                  <div className="success-message">
                    {emailSuccess}
                  </div>
                )}
                {error && (
                  <div className="error-message" style={{ color: '#f44336', marginTop: '10px' }}>
                    {error}
                  </div>
                )}
              </div>
              <div className="modal-footer">
                <button 
                  className="modal-button cancel"
                  onClick={handleCloseEmailModal}
                  disabled={isSendingEmail}
                >
                  Cancel
                </button>
                <button 
                  className="modal-button send"
                  onClick={handleSendEmail}
                  disabled={isSendingEmail}
                >
                  {isSendingEmail ? 'Sending PDF…' : 'Send PDF via Email'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        * {
          font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .app-container {
          display: grid;
          grid-template-columns: 1fr 1.1fr 0.8fr;
          gap: 12px;
          height: 100vh;
          padding: 12px;
          background: #f7f7f8;
        }

        /* Decorative Background Elements */
        .bg-decoration {
          display: none;
        }

        .sun-icon {
          position: absolute;
          top: 5%;
          right: 10%;
          font-size: 4rem;
          animation: rotate 20s linear infinite;
          filter: drop-shadow(0 0 20px rgba(255, 200, 0, 0.5));
        }

        .plane-icon {
          position: absolute;
          top: 20%;
          left: -50px;
          font-size: 2rem;
          animation: flyAcross 15s linear infinite;
        }

        .cloud-icon {
          position: absolute;
          font-size: 3rem;
          opacity: 0.3;
          animation: float 8s ease-in-out infinite;
        }

        .cloud-1 {
          top: 15%;
          left: 20%;
        }

        .cloud-2 {
          top: 60%;
          right: 15%;
          animation-delay: 4s;
        }

        .palm-icon {
          position: absolute;
          bottom: 10%;
          left: 5%;
          font-size: 3rem;
          animation: sway 3s ease-in-out infinite;
        }

        @keyframes rotate {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        @keyframes flyAcross {
          0% { left: -50px; top: 20%; }
          50% { top: 25%; }
          100% { left: 110%; top: 20%; }
        }

        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }

        @keyframes sway {
          0%, 100% { transform: rotate(-5deg); }
          50% { transform: rotate(5deg); }
        }

        /* CHAT PANEL */
        .chat-panel {
          display: flex;
          flex-direction: column;
          background: #ffffff;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
          overflow: hidden;
        }

        .chat-header {
          padding: 1rem 1.25rem;
          background: #ffffff;
          color: #111827;
          border-bottom: 1px solid #e5e7eb;
        }

        @keyframes gradientShift {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 0.25rem;
        }

        .logo-icon {
          font-size: 1.75rem;
        }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        @keyframes bounce {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }

        .logo-text {
          margin: 0;
          font-size: 1.5rem;
          font-weight: 700;
          letter-spacing: 0.02em;
          color: #111827;
        }

        .tagline {
          margin: 0;
          font-size: 0.9rem;
          color: #6b7280;
        }

        .status-row {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-top: 0.5rem;
          flex-wrap: wrap;
        }

        .status-badge {
          font-size: 0.75rem;
          padding: 0.25rem 0.5rem;
          border-radius: 999px;
          font-weight: 500;
        }

        .status-badge.connected {
          background: #dcfce7;
          color: #166534;
        }

        .status-badge.warning {
          background: #fef3c7;
          color: #92400e;
        }

        .header-icons {
          display: none;
        }

        .header-icons span:nth-child(1) { animation-delay: 0.1s; }
        .header-icons span:nth-child(2) { animation-delay: 0.2s; }
        .header-icons span:nth-child(3) { animation-delay: 0.3s; }
        .header-icons span:nth-child(4) { animation-delay: 0.4s; }

        @keyframes popIn {
          0% { transform: scale(0); opacity: 0; }
          70% { transform: scale(1.2); }
          100% { transform: scale(1); opacity: 1; }
        }

        .messages-container {
          flex: 1;
          overflow-y: auto;
          padding: 1.5rem;
          background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
          background-attachment: fixed;
        }

        .message {
          display: flex;
          gap: 1rem;
          margin-bottom: 1.5rem;
          animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .message.user {
          flex-direction: row-reverse;
        }

        .message-avatar {
          width: 45px;
          height: 45px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1.6rem;
          flex-shrink: 0;
          background: linear-gradient(135deg, #FFE66D 0%, #4ECDC4 100%);
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          border: 3px solid white;
        }

        .message.user .message-avatar {
          background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        }

        .message-content {
          max-width: 70%;
        }

        .message-text {
          padding: 1rem 1.25rem;
          border-radius: 1.25rem;
          line-height: 1.5;
          white-space: pre-wrap;
        }

        .message.assistant .message-text {
          background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
          color: #2d3748;
          border-bottom-left-radius: 0.25rem;
          box-shadow: 0 4px 15px rgba(0,0,0,0.12);
          border: 2px solid #e9ecef;
        }

        .message.user .message-text {
          background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
          color: white;
          border-bottom-right-radius: 0.25rem;
          box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        }

        .message-time {
          font-size: 0.75rem;
          color: #a0aec0;
          margin-top: 0.25rem;
          padding: 0 0.5rem;
        }

        .typing-indicator {
          display: flex;
          gap: 0.25rem;
          padding: 1rem 1.25rem;
          background: white;
          border-radius: 1.25rem;
          border-bottom-left-radius: 0.25rem;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #cbd5e0;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
        .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }

        .error-banner {
          padding: 1rem;
          background: #fed7d7;
          color: #c53030;
          text-align: center;
          font-size: 0.9rem;
        }

        .input-container {
          display: flex;
          gap: 0.75rem;
          padding: 1.5rem;
          background: white;
          border-top: 1px solid #e2e8f0;
        }

        .chat-input {
          flex: 1;
          padding: 0.875rem 1.25rem;
          border: 2px solid #e2e8f0;
          border-radius: 1.5rem;
          font-size: 1rem;
          outline: none;
          transition: all 0.2s;
        }

        .chat-input:focus {
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .voice-button, .send-button {
          width: 50px;
          height: 50px;
          border: none;
          border-radius: 50%;
          font-size: 1.5rem;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .voice-button {
          background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
          color: white;
          box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        }

        .voice-button.listening {
          background: linear-gradient(135deg, #f56565 0%, #ff4757 100%);
          animation: pulseGlow 1s infinite;
        }

        @keyframes pulseGlow {
          0%, 100% { 
            transform: scale(1); 
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
          }
          50% { 
            transform: scale(1.15); 
            box-shadow: 0 8px 25px rgba(255, 71, 87, 0.6);
          }
        }

        .send-button {
          background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
          color: white;
          box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
        }

        .voice-button:hover, .send-button:hover {
          transform: scale(1.05);
        }

        .voice-button:disabled, .send-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none;
        }

        /* ITINERARY PANEL */
        .itinerary-panel {
          display: flex;
          flex-direction: column;
          background: #ffffff;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.06);
          overflow: hidden;
        }

        .sources-panel {
          display: flex;
          flex-direction: column;
          background: #ffffff;
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.06);
          overflow: hidden;
        }

        .itinerary-header {
          padding: 1rem 1.25rem;
          background: #ffffff;
          color: #111827;
          border-bottom: 1px solid #e5e7eb;
        }

        .polaroid-title,
        .title-decoration,
        .deco-element {
          display: none;
        }

        .itinerary-main-title {
          margin: 0;
          font-size: 1.25rem;
          font-weight: 600;
          color: #111827;
        }

        .itinerary-title-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          position: relative;
          z-index: 1;
        }

        .email-button-new {
          background: #111827;
          color: #ffffff;
          border: none;
          padding: 0.5rem 0.9rem;
          border-radius: 8px;
          font-weight: 600;
          font-size: 0.9rem;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 0.4rem;
        }

        .email-button-new:hover {
          background: #1f2937;
          transform: none;
          box-shadow: none;
        }

        .email-icon {
          font-size: 1rem;
          animation: none;
        }

        @keyframes shake {
          0%, 100% { transform: rotate(0deg); }
          10%, 30% { transform: rotate(-10deg); }
          20%, 40% { transform: rotate(10deg); }
        }

        .itinerary-stats {
          display: flex;
          gap: 0.5rem;
          flex-wrap: wrap;
        }

        .stat-badge {
          display: flex;
          align-items: center;
          gap: 0.4rem;
          background: #f3f4f6;
          padding: 0.35rem 0.6rem;
          border-radius: 999px;
          font-weight: 600;
          font-size: 0.85rem;
          color: #111827;
        }

        .stat-badge:hover {
          transform: none;
          background: #e5e7eb;
        }

        .stat-icon {
          font-size: 1rem;
          animation: none;
        }

        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1); }
        }

        .itinerary-content {
          flex: 1;
          overflow-y: auto;
          padding: 2rem;
          background: linear-gradient(to bottom, #FFF9E5 0%, #F8F9FA 100%);
          background-attachment: fixed;
        }

        /* Polaroid Card Styling */
        .day-card-polaroid {
          background: white;
          padding: 1rem 1rem 2rem 1rem;
          margin-bottom: 2rem;
          box-shadow: 0 8px 25px rgba(0,0,0,0.15);
          transition: all 0.3s;
          position: relative;
          transform: rotate(-1deg);
        }

        .day-card-polaroid:nth-child(even) {
          transform: rotate(1deg);
        }

        .day-card-polaroid:hover {
          transform: rotate(0deg) translateY(-10px) scale(1.02);
          box-shadow: 0 15px 40px rgba(0,0,0,0.25);
          z-index: 10;
        }

        .polaroid-top {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 1rem;
        }

        .tape {
          position: absolute;
          width: 80px;
          height: 30px;
          background: rgba(255, 220, 150, 0.6);
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          transform: rotate(-5deg);
        }

        .tape-left {
          left: 1rem;
          top: -0.5rem;
        }

        .tape-right {
          right: 1rem;
          top: -0.5rem;
          transform: rotate(5deg);
        }

        .polaroid-caption {
          text-align: center;
          margin-top: 0.75rem;
          font-family: 'Pacifico', cursive;
          color: #555;
          font-size: 1.1rem;
        }

        .day-card {
          background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
          border-radius: 1rem;
          padding: 1.5rem;
          border: 3px solid #f0f0f0;
        }

        .day-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1.5rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #f1f5f9;
        }

        .day-title {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .day-badge {
          font-size: 1.8rem;
          font-weight: 800;
          background: linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          display: inline-block;
        }

        .day-date {
          font-size: 1rem;
          color: #64748b;
          font-weight: 500;
        }

        .feasibility-badge-new {
          padding: 0.6rem 1.2rem;
          border-radius: 2rem;
          color: white;
          font-weight: 700;
          font-size: 0.9rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .badge-icon {
          font-size: 1.1rem;
          animation: checkmark 1s ease-in-out infinite;
        }

        @keyframes checkmark {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.2); }
        }

        .day-blocks {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .time-block {
          padding: 1rem;
          border-radius: 0.875rem;
          border-left: 4px solid;
        }

        .time-block.morning {
          background: linear-gradient(135deg, #FFF4E6 0%, #FFE6CC 100%);
          border-color: #FF9966;
          border-width: 3px;
        }

        .time-block.afternoon {
          background: linear-gradient(135deg, #FFF9C4 0%, #FFF59D 100%);
          border-color: #FFD54F;
          border-width: 3px;
        }

        .time-block.evening {
          background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
          border-color: #64B5F6;
          border-width: 3px;
        }

        .block-header {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.75rem;
          font-weight: 600;
          color: #1e293b;
        }

        .block-icon {
          font-size: 1.25rem;
        }

        .block-time {
          font-size: 0.9rem;
        }

        .block-pois {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin-left: 1.75rem;
        }

        .poi-item {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          gap: 0.5rem;
        }

        .poi-name {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: #334155;
          font-size: 0.95rem;
        }

        .poi-bullet {
          color: #94a3b8;
        }

        .poi-duration {
          font-size: 0.85rem;
          color: #64748b;
          background: white;
          padding: 0.25rem 0.75rem;
          border-radius: 1rem;
        }
        
        .poi-rag-description {
          font-size: 0.85rem;
          color: #475569;
          background: #f1f5f9;
          padding: 0.5rem;
          border-radius: 0.5rem;
          margin-top: 0.5rem;
          border-left: 3px solid #3b82f6;
          font-style: italic;
        }

        .travel-info {
          margin-top: 0.75rem;
          margin-left: 1.75rem;
          font-size: 0.85rem;
          color: #64748b;
        }

        .day-footer {
          margin-top: 1rem;
          padding-top: 1rem;
          padding: 0.75rem;
          background: rgba(255, 107, 107, 0.1);
          border-radius: 0.75rem;
          border-left: 4px solid #FF6B6B;
          font-size: 0.9rem;
          color: #FF6B6B;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .footer-icon {
          font-size: 1.2rem;
        }

        /* SOURCES SECTION */
        .sources-section {
          background: #ffffff;
          border-radius: 8px;
          padding: 0;
          box-shadow: none;
          border: none;
          position: relative;
          overflow: hidden;
        }

        .sources-section::before {
          content: none;
        }

        .sources-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.75rem;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid #e5e7eb;
        }

        .sources-header h3 {
          margin: 0;
          font-size: 1rem;
          font-weight: 600;
          color: #111827;
          display: flex;
          align-items: center;
          gap: 0.4rem;
        }

        .sources-count {
          background: #f3f4f6;
          color: #111827;
          padding: 0.2rem 0.6rem;
          border-radius: 999px;
          font-size: 0.85rem;
          font-weight: 600;
          box-shadow: none;
        }

        .sources-content {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          max-height: 200px;
          overflow-y: auto;
          padding-right: 0.5rem;
        }

        .sources-empty {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          padding: 1rem;
          color: #6b7280;
        }
        
        .sources-empty h3 {
          margin: 0;
          font-size: 1rem;
          font-weight: 600;
          color: #111827;
        }
        
        .sources-empty p {
          margin: 0;
          font-size: 0.9rem;
          color: #6b7280;
        }

        .source-card {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          background: #ffffff;
          padding: 0.75rem;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
          box-shadow: none;
          cursor: default;
        }

        .source-card:hover {
          transform: none;
          box-shadow: none;
          background: #f9fafb;
        }

        .source-icon {
          font-size: 2rem;
          flex-shrink: 0;
          animation: bounce 2s ease-in-out infinite;
        }

        .source-card:nth-child(2) .source-icon {
          animation-delay: 0.2s;
        }

        .source-card:nth-child(3) .source-icon {
          animation-delay: 0.4s;
        }

        .source-text {
          flex: 1;
          font-weight: 500;
          color: #2E7D32;
        }
        
        .source-name {
          font-weight: 600;
          margin-bottom: 0.25rem;
        }
        
        .source-poi {
          font-size: 0.85rem;
          color: #64748b;
          margin-top: 0.25rem;
        }
        
        .source-section {
          font-size: 0.85rem;
          color: #64748b;
          margin-top: 0.25rem;
          text-transform: capitalize;
          line-height: 1.4;
          word-break: break-word;
        }

        .sources-content::-webkit-scrollbar {
          width: 6px;
        }

        .sources-content::-webkit-scrollbar-track {
          background: #E8F5E9;
          border-radius: 3px;
        }

        .sources-content::-webkit-scrollbar-thumb {
          background: #4CAF50;
          border-radius: 3px;
        }

        .sources-content::-webkit-scrollbar-thumb:hover {
          background: #388E3C;
        }

        .itinerary-placeholder {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          padding: 1rem;
          text-align: center;
          position: relative;
        }

        .placeholder-animation {
          position: relative;
          margin-bottom: 2rem;
        }

        .placeholder-icon-large {
          font-size: 8rem;
          animation: float 3s ease-in-out infinite;
          filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));
        }

        .floating-icons {
          position: absolute;
          width: 200px;
          height: 200px;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        }

        .floating-icons span {
          position: absolute;
          font-size: 2.5rem;
          animation: orbit 8s linear infinite;
        }

        .float-1 { animation-delay: 0s; }
        .float-2 { animation-delay: 1.6s; }
        .float-3 { animation-delay: 3.2s; }
        .float-4 { animation-delay: 4.8s; }
        .float-5 { animation-delay: 6.4s; }

        @keyframes orbit {
          from { transform: rotate(0deg) translateX(100px) rotate(0deg); }
          to { transform: rotate(360deg) translateX(100px) rotate(-360deg); }
        }

        .placeholder-title {
          font-size: 2.5rem;
          font-weight: 800;
          background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin-bottom: 1rem;
          font-family: 'Pacifico', cursive;
        }

        .placeholder-subtitle {
          font-size: 1.2rem;
          color: #64748b;
          margin-bottom: 3rem;
          font-weight: 500;
        }

        .example-queries-new {
          background: white;
          padding: 2rem;
          border-radius: 1.5rem;
          box-shadow: 0 10px 30px rgba(0,0,0,0.15);
          max-width: 500px;
          transform: rotate(-1deg);
          transition: all 0.3s;
        }

        .example-queries-new:hover {
          transform: rotate(0deg) scale(1.05);
          box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }

        .example-header {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 1rem;
          margin-bottom: 1.5rem;
          font-size: 1.2rem;
          font-weight: 700;
          color: #1e293b;
        }

        .mic-pulse {
          font-size: 2rem;
          animation: pulse 1.5s ease-in-out infinite;
        }

        .example-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .example-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
          border-radius: 1rem;
          border-left: 4px solid #FF6B6B;
          transition: all 0.3s;
          cursor: pointer;
        }

        .example-item:hover {
          transform: translateX(10px);
          background: linear-gradient(135deg, #FFE6E6 0%, #FFF 100%);
          box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);
        }

        .example-icon {
          font-size: 2rem;
          flex-shrink: 0;
        }

        .example-item span:last-child {
          color: #64748b;
          font-weight: 500;
        }

        /* Email Modal */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.6);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          animation: fadeIn 0.2s ease;
        }

        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        .modal-content {
          background: white;
          border-radius: 1.5rem;
          width: 90%;
          max-width: 500px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
          from { 
            opacity: 0;
            transform: translateY(20px);
          }
          to { 
            opacity: 1;
            transform: translateY(0);
          }
        }

        .modal-header {
          padding: 1.5rem 2rem;
          border-bottom: 1px solid #e2e8f0;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .modal-header h3 {
          margin: 0;
          font-size: 1.5rem;
          color: #1e293b;
        }

        .modal-close {
          background: none;
          border: none;
          font-size: 2rem;
          color: #64748b;
          cursor: pointer;
          line-height: 1;
          padding: 0;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: all 0.2s;
        }

        .modal-close:hover {
          background: #f1f5f9;
          color: #1e293b;
        }

        .modal-body {
          padding: 2rem;
        }

        .modal-description {
          margin: 0 0 1.5rem 0;
          color: #64748b;
        }

        .email-info {
          background: #f5f7fa;
          padding: 16px;
          border-radius: 8px;
          margin-bottom: 20px;
        }

        .email-info-row {
          margin: 8px 0;
          font-size: 14px;
          color: #374151;
        }

        .email-info-row strong {
          color: #111827;
          margin-right: 8px;
        }

        .email-input-row {
          margin: 12px 0;
        }

        .email-input-row label {
          display: block;
          font-size: 0.9rem;
          font-weight: 600;
          color: #374151;
          margin-bottom: 6px;
        }

        .email-input {
          width: 100%;
          padding: 0.6rem 0.75rem;
          border: 2px solid #e2e8f0;
          border-radius: 8px;
          font-size: 1rem;
          outline: none;
          transition: border-color 0.2s;
        }

        .email-input:focus {
          border-color: #667eea;
        }

        .email-input::placeholder {
          color: #94a3b8;
        }

        .email-default {
          font-size: 0.85rem;
          color: #64748b;
          margin-top: 4px;
        }

        .success-message {
          margin-top: 1rem;
          padding: 1rem;
          background: #dcfce7;
          color: #166534;
          border-radius: 0.75rem;
          text-align: center;
          font-weight: 500;
        }

        .modal-footer {
          padding: 1.5rem 2rem;
          border-top: 1px solid #e2e8f0;
          display: flex;
          gap: 1rem;
          justify-content: flex-end;
        }

        .modal-button {
          padding: 0.75rem 1.5rem;
          border: none;
          border-radius: 0.75rem;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .modal-button.cancel {
          background: #f1f5f9;
          color: #64748b;
        }

        .modal-button.cancel:hover {
          background: #e2e8f0;
        }

        .modal-button.send {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .modal-button.send:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .modal-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none;
        }

        /* Scrollbar */
        .messages-container::-webkit-scrollbar,
        .itinerary-content::-webkit-scrollbar {
          width: 8px;
        }

        .messages-container::-webkit-scrollbar-track,
        .itinerary-content::-webkit-scrollbar-track {
          background: #f1f5f9;
        }

        .messages-container::-webkit-scrollbar-thumb,
        .itinerary-content::-webkit-scrollbar-thumb {
          background: #cbd5e0;
          border-radius: 4px;
        }

        .messages-container::-webkit-scrollbar-thumb:hover,
        .itinerary-content::-webkit-scrollbar-thumb:hover {
          background: #a0aec0;
        }

        /* Responsive */
        @media (max-width: 1024px) {
          .app-container {
            grid-template-columns: 1fr;
            height: auto;
          }
          
          .chat-panel {
            height: auto;
          }
        }
      `}</style>
    </>
  );
}
