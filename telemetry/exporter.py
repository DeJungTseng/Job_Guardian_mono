
import logging
import json
from rich.logging import RichHandler
import os

# Create the telemetry directory if it doesn't exist
if not os.path.exists('telemetry'):
    os.makedirs('telemetry')

log_file_path = os.path.join('telemetry', 'mcp-activity.log')

# Configure the logger
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("rich")

# Add a file handler to log to a JSONL file
file_handler = logging.FileHandler(log_file_path)

class JsonlFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if isinstance(record.args, dict):
            log_record["data"] = record.args
        return json.dumps(log_record)

file_handler.setFormatter(JsonlFormatter())
logger.addHandler(file_handler)

def get_logger(name):
    """
    Returns a logger instance with the specified name.
    """
    return logging.getLogger(name)

# Example usage:
if __name__ == '__main__':
    main_logger = get_logger("MCPAggregator.job_guardian")
    main_logger.info("Requesting tool call", {'tool_name': 'some_tool', 'server_name': 'some_server'})
    main_logger.info("Another log message")
