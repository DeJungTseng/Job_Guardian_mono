
'use client';

import { useEffect, useState } from 'react';

interface LogEntry {
  prefix: string;
  data: any;
}

// No longer needed as we directly use prefix
// const messageMapping: { [key: string]: string } = {
//   "Entering span: receive_prompt": "LLM receiving prompt...",
//   "Requesting tool call": "Requesting tool call...",
//   "Exiting span: llm_tool_call_and_synthesis, duration": "Tool call response received.",
//   "Entering span: format_response": "Forming structural response to user...",
// };

export function TelemetryStream() {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5001/telemetry/stream');

    eventSource.onmessage = (event) => {
      try {
        const logEntry: LogEntry = JSON.parse(event.data);
        // We can directly use the prefix from the logEntry
        // Or further parse logEntry.prefix to extract level and message if needed
        setLogs((prevLogs) => [...prevLogs, logEntry]);
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
          {/* Display the prefix directly, or parse it further if desired */}
          <span dangerouslySetInnerHTML={{ __html: log.prefix }} />
          {/* Optionally display some data from log.data if needed */}
          {/* <pre>{JSON.stringify(log.data, null, 2)}</pre> */}
        </div>
      ))}
    </div>
  );
}
