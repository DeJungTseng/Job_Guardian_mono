
from functools import wraps
from telemetry.exporter import get_logger
import time

logger = get_logger("tracing")

def trace_span(span_name):
    """
    A decorator to trace the execution of a function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Entering span: {span_name}")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"Exiting span: {span_name}, duration: {end_time - start_time:.2f}s")
            return result
        return wrapper
    return decorator
