
from functools import wraps
from telemetry.exporter import log_queue
import time
import json

def trace_span(span_name):
    """
    A decorator to trace the execution of a function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_queue.put(json.dumps({"level": "INFO", "name": "tracing", "message": f"Entering span: {span_name}"}))
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            log_queue.put(json.dumps({"level": "INFO", "name": "tracing", "message": f"Exiting span: {span_name}, duration: {end_time - start_time:.2f}s"}))
            return result
        return wrapper
    return decorator
