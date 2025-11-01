import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import os
import aiofiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "mcp-activity.log")

@app.get("/telemetry/stream")
async def stream_telemetry():
    """
    Streams telemetry data using Server-Sent Events (SSE) by tailing the log file.
    """
    async def event_generator():
        # Ensure the log file exists
        if not os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "w") as f:
                f.write("") # Create an empty file

        async with aiofiles.open(LOG_FILE_PATH, mode="r") as f:
            current_position = await f.tell()
            while True:
                await asyncio.sleep(0.1)  # Wait for new lines
                # Check if the file has grown
                new_size = os.path.getsize(LOG_FILE_PATH)
                if new_size > current_position:
                    await f.seek(current_position) # Seek to the last known position
                    line = await f.readline()
                    while line:
                        yield f"data: {line.strip()}\n\n"
                        current_position = await f.tell()
                        line = await f.readline()
                elif new_size < current_position: # File was truncated or reset
                    await f.seek(0)
                    current_position = 0

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/telemetry/recent")
async def get_recent_telemetry():
    """
    Returns the last few lines of the telemetry log file.
    """
    if not os.path.exists(LOG_FILE_PATH):
        return {"data": "Log file not found"}

    lines = []
    async with aiofiles.open(LOG_FILE_PATH, mode="r") as f:
        # Read last 50 lines for example
        # This is a simplified approach, for very large files, more efficient tailing might be needed
        content = await f.read()
        lines = content.splitlines()[-50:]

    return {"data": "\n".join(lines)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
