"use client";

import React from 'react';

interface LiveTranscriptProps {
  transcript: string;
  isListening: boolean;
}

export default function LiveTranscript({ transcript, isListening }: LiveTranscriptProps) {
  return (
    <div className="transcript-container">
      <h3 className="transcript-title">Live Transcript</h3>
      <div className={`transcript-box ${isListening ? 'listening' : ''}`}>
        {transcript || (
          <span className="transcript-placeholder">
            {isListening ? 'Listening...' : 'Click microphone to start'}
          </span>
        )}
      </div>
    </div>
  );
}
