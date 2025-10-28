
import uvicorn
from fastapi import FastAPI, Response
import os

app = FastAPI()

LOG_FILE = os.path.join(os.path.dirname(__file__), "mcp-activity.log")

@app.get("/telemetry/recent")
def recent_trace():
    """
    Return the most recent 10 log entries from the telemetry log file.
    """
    if not os.path.exists(LOG_FILE):
        return Response(content="Log file not found.", status_code=404)

    try:
        with open(LOG_FILE, "r") as f:
            # Read the last N lines of the file
            lines = f.readlines()
            last_10_lines = lines[-10:]
            return Response(content="".join(last_10_lines), media_type="text/plain")
    except Exception as e:
        return Response(content=f"Error reading log file: {e}", status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
