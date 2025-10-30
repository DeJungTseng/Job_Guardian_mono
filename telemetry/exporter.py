


import logging

import json

import queue

from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from opentelemetry.trace import Span



# Create a queue to hold log messages

log_queue = queue.Queue()



logger = logging.getLogger("telemetry_logger")



class QueueSpanExporter(SpanExporter):

    def __init__(self):

        super().__init__()



    def export(self, spans: list[Span]) -> SpanExportResult:

        for span in spans:

            log_queue.put(span.to_json())

        return SpanExportResult.SUCCESS



    def shutdown(self):

        pass



def get_exporter():

    """

    Returns a span exporter.

    """

    return QueueSpanExporter()



def get_logger():

    """

    Returns a logger instance with the specified name.

    """

    return logger
