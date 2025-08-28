'use client'; // This ensures it's client-side only

import React, { useState, useEffect } from 'react';

interface MessageTimestampProps {
  timestamp: string; // Expect an ISO string (e.g., "2025-08-20T14:22:00Z")
}

const MessageTimestamp: React.FC<MessageTimestampProps> = ({ timestamp }) => {
  const [clientTime, setClientTime] = useState<string>('');

  useEffect(() => {
    if (timestamp) {
      // Format the time only on the client
      const timeString = new Date(timestamp).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      });
      setClientTime(timeString);
    }
  }, [timestamp]);

  return <span>{clientTime}</span>; // Renders the formatted time (e.g., "02:22 PM")
};

export default MessageTimestamp;
