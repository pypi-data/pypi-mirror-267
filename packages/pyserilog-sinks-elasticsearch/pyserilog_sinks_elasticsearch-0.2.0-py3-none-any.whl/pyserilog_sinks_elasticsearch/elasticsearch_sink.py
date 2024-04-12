from pyserilog.core.ilog_event_sink import ILogEventSink
from pyserilog.core.string_writable import StringIOWriteable
from pyserilog.events.log_event import LogEvent
from pyserilog.sinks.periodic_batching.options import PeriodicBatchingSinkOptions
from pyserilog.sinks.periodic_batching.periodic_batching_sink import IBatchedLogEventSink, PeriodicPatchingSink

from pyserilog_sinks_elasticsearch.sinks.elasticsearch_sink_state import ElasticsearchSinkState
from pyserilog_sinks_elasticsearch.sinks.options import ElasticsearchSinkOptions, RegisterTemplateRecovery
from elasticsearch import helpers


class BatchedElasticsearchSink(IBatchedLogEventSink):

    def __init__(self, options: ElasticsearchSinkOptions):
        self._state = ElasticsearchSinkState.create(options)
        self._state.register_template_if_needed()

    def emit_batch(self, events: list[LogEvent]) -> None:
        try:
            self._emit_batch_checked(events)
        except Exception as e:
            print(e)

    def on_empty_batch(self) -> None:
        pass

    def _emit_batch_checked(self, events: list[LogEvent]) -> None:
        if events is None or len(events) == 0:
            return

        payload = self._create_payload(events)
        helpers.bulk(self._state.client, payload)

    def _create_payload(self, events: list[LogEvent]) -> list[dict] | None:
        if self._state.template_registration_success is False and self._state.options.register_template == RegisterTemplateRecovery.FAIL_SINK:
            return None

        payload = []
        for event in events:
            index_name = self._state.get_index_for_event(event, event.timestamp)

            res = dict()
            res["_index"] = index_name
            res["_op_type"] = "index"
            with StringIOWriteable() as sw:
                self._state.formatter.format(event, sw)
                res["_source"] = sw.getvalue()
            payload.append(res)
        return payload


class ElasticsearchSink(ILogEventSink):

    def __init__(self, options: ElasticsearchSinkOptions):
        sink = BatchedElasticsearchSink(options)
        sink_options = PeriodicBatchingSinkOptions(
            period=options.period,
            eagerly_emit_first_event=True,
            queue_limit=options.queue_size_limit if (options.queue_size_limit is not None and options.queue_size_limit > 0) else 10000,
            batch_size_limit=options.batch_posting_limit
        )
        self._batching_sink = PeriodicPatchingSink(sink, sink_options)

    def __enter__(self):
        self._batching_sink.__enter__()
        return self

    def emit(self, log_event: LogEvent):
        self._batching_sink.emit(log_event)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._batching_sink.__exit__(exc_type, exc_val, exc_tb)
