import uvicorn
from fastapi import FastAPI, Response
import subprocess
import logging
import os
from telemetry.tracing import trace_span

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

LOG_FILE = os.path.join('telemetry', 'mcp-activity.log')

@app.get("/logs")
def get_logs():
    """
    Endpoint to retrieve the latest 50 log entries.
    """
    if not os.path.exists(LOG_FILE):
        return Response(content="Log file not found.", status_code=404)

    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            last_50_lines = lines[-50:]
            return Response(content="".join(last_50_lines), media_type="text/plain")
    except Exception as e:
        return Response(content=f"Error reading log file: {e}", status_code=500)

@trace_span("receive_prompt")
def receive_prompt(user_query: str):
    """
    Placeholder for receiving a prompt.
    """
    logger.info(f"Received prompt: {user_query}")
    return user_query

@trace_span("llm_tool_call_and_synthesis")
def llm_tool_call_and_synthesis(prompt: str):
    """
    Placeholder for LLM tool call and synthesis.
    """
    logger.info(f"Performing LLM tool call and synthesis for: {prompt}")
    return f"LLM response for: {prompt}"

@trace_span("format_response")
def format_response(llm_response: str):
    """
    Placeholder for formatting the response.
    """
    logger.info(f"Formatting response: {llm_response}")
    return {"result": llm_response}

@app.post("/query")
async def query_agent(query: dict):
    """
    Endpoint to send a query to the agent.
    """
    user_query = query.get("query")
    if not user_query:
        return {"error": "Query not provided"}
    
    prompt = receive_prompt(user_query)
    llm_response = llm_tool_call_and_synthesis(prompt)
    response = format_response(llm_response)
    
    return response

@app.on_event("startup")
async def startup_event():
    """
    Start all background processes and initialize the agent.
    """
    # Start the telemetry server
    logger.info("Starting telemetry server...")
    try:
        subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), "telemetry", "telemetry_server.py")])
        logger.info("Telemetry server started.")
    except FileNotFoundError:
        logger.error("Could not find telemetry_server.py. Make sure the path is correct.")
    except Exception as e:
        logger.error(f"Failed to start telemetry server: {e}")

    # Initialize the agent
    logger.info("Initializing agent...")
    # Placeholder for agent initialization
    logger.info("✅ Agent ready")

# Mount the static files at the end
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend/out", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)