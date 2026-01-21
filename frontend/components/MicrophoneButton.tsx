"use client";

import React, { useState, useRef, useEffect } from 'react';

interface MicrophoneButtonProps {
  onTranscript: (text: string) => void;
  onError?: (error: string) => void;
}

export default function MicrophoneButton({ onTranscript, onError }: MicrophoneButtonProps) {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Check if browser supports Web Speech API
    const SpeechRecognition = (window as any).SpeechRecognition || 
                              (window as any).webkitSpeechRecognition;
    
    if (SpeechRecognition) {
      setIsSupported(true);
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript + ' ';
          } else {
            interimTranscript += transcript;
          }
        }

        if (finalTranscript) {
          onTranscript(finalTranscript.trim());
        }
      };

      recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        if (onError) {
          onError(`Speech recognition error: ${event.error}`);
        }
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    } else {
      setIsSupported(false);
      if (onError) {
        onError('Speech recognition not supported in this browser. Please use Chrome or Edge.');
      }
    }
  }, [onTranscript, onError]);

  const toggleListening = () => {
    if (!recognitionRef.current) return;

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  if (!isSupported) {
    return (
      <div className="mic-button-container">
        <button disabled className="mic-button disabled">
          🎤 Microphone not supported
        </button>
        <p className="text-sm text-gray-500">
          Please use Chrome or Edge browser for voice input
        </p>
      </div>
    );
  }

  return (
    <div className="mic-button-container">
      <button
        onClick={toggleListening}
        className={`mic-button ${isListening ? 'listening' : ''}`}
        aria-label={isListening ? 'Stop listening' : 'Start listening'}
      >
        {isListening ? '🛑 Stop' : '🎤 Start'}
      </button>
      {isListening && (
        <div className="listening-indicator">
          <span className="pulse-dot"></span>
          Listening...
        </div>
      )}
    </div>
  );
}
