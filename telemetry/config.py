from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from telemetry.exporter import get_exporter


def setup_telemetry(service_name: str = "job_guardian_backend"):
    """初始化 OpenTelemetry Provider 與 Exporter"""
    # 建立 provider
    provider = TracerProvider()
    
    # 使用我們的 get_exporter() 取得正確輸出端 (用於檔案和終端輸出)
    activity_exporter = get_exporter()
    provider.add_span_processor(BatchSpanProcessor(activity_exporter))

    # 設定全域 tracer provider
    trace.set_tracer_provider(provider)

    # 回傳 Tracer
    return trace.get_tracer(service_name)
