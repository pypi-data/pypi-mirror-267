import inspect
from datetime import datetime

import sys
from pyserilog.core.string_writable import StringWriteable
from pyserilog.events.log_event_level import LogEventLevel
from pyserilog.events.log_event_property_value import LogEventPropertyValue
from pyserilog.events.message_template import MessageTemplate

from .conf.config import Config
from .utils import varmap
from .utils.encoding import to_unicode, shorten, keyword_field
from .utils.stacks import get_stack_info, iter_traceback_frames
import pyserilog_formating_elasticsearch.utils.processors as processors

from pyserilog_formating_elasticsearch.default_json_formatter import DefaultJsonFormatter

RENDERED_MESSAGE_PROPERTY_NAME = "message"
MESSAGE_TEMPLATE_PROPERTY_NAME = "messageTemplate"
EXCEPTION_PROPERTY_NAME = "Exception"
LEVEL_PROPERTY_NAME = "level"
TIMESTAMP_PROPERTY_NAME = "@timestamp"


class ElasticsearchJsonFormatter(DefaultJsonFormatter):
    def __init__(self,
                 omit_enclosing_object=False,
                 closing_delimiter=None,
                 render_message=True,
                 render_message_template=True,
                 inline_fields: bool = False,
                 config: Config = None
                 ):
        super().__init__(omit_enclosing_object, closing_delimiter, render_message, render_message_template)
        self._config = config if config else Config()
        self.inline_fields: bool = inline_fields

        def is_processor_function(x):
            return inspect.isfunction(x) and hasattr(x, "event_types")

        self._processors = inspect.getmembers(processors, is_processor_function)

    def write_timestamp(self, timestamp: datetime, preceding_delimiter: str, output: StringWriteable) -> str:
        return self.write_json_property(TIMESTAMP_PROPERTY_NAME, timestamp, preceding_delimiter, output)

    def write_level(self, level: LogEventLevel, preceding_delimiter: str, output: StringWriteable) -> str:
        level_str = str(level.name)
        return self.write_json_property(LEVEL_PROPERTY_NAME, level_str, preceding_delimiter, output)

    def write_message_template(self, template: MessageTemplate, delim: str, output: StringWriteable):
        return self.write_json_property(MESSAGE_TEMPLATE_PROPERTY_NAME, template, delim, output)

    def write_rendered_message(self, template: str, delim: str, output: StringWriteable):
        return self.write_json_property(RENDERED_MESSAGE_PROPERTY_NAME, template, delim, output)

    def write_exception(self, exception: Exception, delim: str, output: StringWriteable):
        data = self.get_exception_serialization_info(exception, 0)
        self._process_exception(data)
        self.write_json_property("exception", data["exception"], delim, output)
        return ","

    def write_properties(self, properties: dict[str, LogEventPropertyValue], output: StringWriteable):
        if not self.inline_fields:
            output.write(",fields:{")
        else:
            output.write(",")
        self.write_properties_values(properties, output)
        if not self.inline_fields:
            output.write("}")

    def get_exception_serialization_info(self, exc_info, depth: int) -> dict:
        new_exc_info, exc_info = self.get_exc_info(exc_info)
        exc_type, exc_value, exc_traceback = exc_info
        message = "%s: %s" % (exc_type, to_unicode(exc_value)) if exc_value else str(exc_type)
        frames = self.get_frames(exc_info)
        if hasattr(exc_type, "__module__"):
            exc_module = exc_type.__module__
            exc_type = exc_type.__name__
        else:
            exc_module = None
            exc_type = exc_type.__name__
        data = {
            "exception": {
                "message": message,
                "type": keyword_field(str(exc_type)),
                "module": keyword_field(str(exc_module)),
                "stacktrace": frames,
            }
        }
        cause = exc_value.__cause__
        chained_context = exc_value.__context__
        # we follow the pattern of Python itself here and only capture the chained exception
        # if cause is not None and __suppress_context__ is False
        if depth < 20 and chained_context and not (exc_value.__suppress_context__ and cause is None):
            if cause:
                exc_type = type(cause)
                exc_value = cause
            else:
                exc_type = type(chained_context)
                exc_value = chained_context
            exc_info = exc_type, exc_value, chained_context.__traceback__
            depth += 1
            chained_cause = self.get_exception_serialization_info(exc_info, depth)
            if chained_cause:
                data["exception"]["cause"] = [chained_cause["exception"]]

        return data

    @staticmethod
    def get_exc_info(exc_info):
        new_exc_info = False
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                new_exc_info = True
                exc_info = sys.exc_info()
        return new_exc_info, exc_info

    def get_frames(self, exc_info):
        exc_type, exc_value, exc_traceback = exc_info
        frames = get_stack_info(
            iter_traceback_frames(exc_traceback, self._config.stack_trace_frames_limit),
            with_locals=self._config.collect_local_variables,
            library_frame_context_lines=self._config.source_lines_error_library_frames,
            in_app_frame_context_lines=self._config.source_lines_error_app_frames,
            include_paths_re=self._config.include_paths_re,
            exclude_paths_re=self._config.exclude_paths_re,
            locals_processor_func=lambda local_var: varmap(
                lambda k, val: shorten(
                    val,
                    list_length=self._config.local_var_list_max_length,
                    string_length=self._config.local_var_max_length,
                    dict_length=self._config.local_var_dict_max_length,
                ),
                local_var,
            ),
        )

        return frames

    def _process_exception(self, frames):
        for processor_name, processor in self._processors:
            if processor.event_types and "error" in processor.event_types:
                try:
                    processor(self._config, frames)
                except Exception as e:
                    print(e)
