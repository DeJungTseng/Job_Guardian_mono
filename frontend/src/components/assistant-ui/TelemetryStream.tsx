
'use client';

import { useEffect, useState } from 'react';

interface LogEntry {
  level: string;
  name: string;
  message: string;
  data?: any;
}

const messageMapping: { [key: string]: string } = {
  "Entering span: receive_prompt": "LLM receiving prompt...",
  "Requesting tool call": "Requesting tool call...",
  "Exiting span: llm_tool_call_and_synthesis, duration": "Tool call response received.",
  "Entering span: format_response": "Forming structural response to user...",
};

export function TelemetryStream() {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5001/telemetry/stream');

    eventSource.onmessage = (event) => {
      try {
        const logEntry = JSON.parse(event.data);
        const mappedMessage = Object.keys(messageMapping).find(key => {
          return logEntry.message.includes(key) || (logEntry.name && logEntry.name.includes(key));
        });
        if (mappedMessage) {
          let message = messageMapping[mappedMessage];
          if (mappedMessage === 'Exiting span: llm_tool_call_and_synthesis, duration') {
            const duration = logEntry.message.split('duration: ')[1];
            message = `${message} <span class="text-yellow-400">[${duration}]</span>`;
          }
          logEntry.message = message;
          setLogs((prevLogs) => [...prevLogs, logEntry]);
        }
      } catch (error) {
        console.error("Failed to parse log entry:", error);
      }
    };

    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div className="h-[180px] w-full overflow-y-auto rounded-lg border border-gray-700 bg-[#0d1117] p-4 font-mono text-sm text-white">
      <div className="font-bold text-lg mb-2">Telemetry Stream</div>
      {logs.map((log, index) => (
        <div key={index}>
          <span className={`font-bold ${log.level === 'INFO' ? 'text-green-500' : 'text-red-500'}`}>{log.level}</span>: <span dangerouslySetInnerHTML={{ __html: log.message }} />
        </div>
      ))}
    </div>
  );
}
