import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
from telemetry.exporter import log_queue

app = FastAPI()


@app.get("/telemetry/stream")
async def stream_telemetry():
    """
    Streams telemetry data using Server-Sent Events (SSE).
    """
    async def event_generator():
        while True:
            if not log_queue.empty():
                log_entry = log_queue.get()
                yield f"data: {log_entry}\n\n"
            await asyncio.sleep(0.1)  # Avoid busy-waiting

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)