'use client';

import { Thread } from '@/components/assistant-ui/thread';
import { TelemetryStream } from '@/components/assistant-ui/TelemetryStream';

export default function Page() {
  return (
    <div className="flex h-screen w-screen flex-col items-center bg-gray-50 font-sans">
      {/* 上方區塊：Assistant-UI 聊天介面 */}
      <div className="flex flex-1 items-center justify-center border-b border-gray-300 bg-white w-full">
        <div className="h-[600px] w-[1000px] overflow-hidden rounded-xl border border-gray-300 shadow-sm">
          <Thread />
        </div>
      </div>

      {/* 下方區塊：Telemetry iframe */}
      <div className="flex w-full items-center justify-center bg-white p-4">
        <div className="h-[180px] w-[1000px] flex items-center justify-center">
          <TelemetryStream />
        </div>
      </div>
    </div>
  );
}
