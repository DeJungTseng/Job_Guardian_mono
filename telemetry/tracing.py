
from functools import wraps
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def trace_span(span_name):
    """
    A decorator to trace the execution of a function using OpenTelemetry.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(span_name):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
