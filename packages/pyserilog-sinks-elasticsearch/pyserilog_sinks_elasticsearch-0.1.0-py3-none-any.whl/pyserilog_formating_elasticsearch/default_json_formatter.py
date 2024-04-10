from abc import ABC
from collections.abc import Callable
from datetime import datetime

from pyserilog import Guard
from pyserilog.core.string_writable import StringWriteable
from pyserilog.events.log_event import LogEvent
from pyserilog.events.log_event_level import LogEventLevel
from pyserilog.formatting import ITextFormatter
from pyserilog.formatting.json.json_value_formatter import JsonValueFormatter
from pyserilog.events.message_template import MessageTemplate
from pyserilog.events.log_event_property_value import LogEventPropertyValue
from pyserilog.events.scalar_value import ScalarValue
from pyserilog.events.sequence_value import SequenceValue
from pyserilog.events.dictionary_value import DictionaryValue


class DefaultJsonFormatter(ITextFormatter, ABC):

    def __init__(self,
                 omit_enclosing_object=False,
                 closing_delimiter=None,
                 render_message=True,
                 render_message_template=True
                 ):
        """
        :param omit_enclosing_object: If true, the properties of the event will be written to the output without
         enclosing braces. Otherwise, if false, each event will be written as a well-formed JSON object
        :param closing_delimiter: A string that will be written after each log event is formatted.
        If null, NewLine will be used. Ignored if omitEnclosingObject is true.
        :param render_message: If true, the message will be rendered and written to
         the output as a property named RenderedMessage.
        :param render_message_template: If true, the message template will be rendered and written to the output as a
        property named RenderedMessageTemplate.
        """
        self._literal_writers: dict[type, Callable[[object, StringWriteable, bool]]] = {
            datetime: lambda x, y, z: self.write_datetime(x, y),
            int: self.write_to_string,
            float: self.write_to_string,
            list: lambda x, y, z: self.write_list(x, y),
            dict: lambda x, y, z: self.write_dict(x, y),
            ScalarValue: lambda x, y, z: self.write_literal(x.value, y, z),
            SequenceValue: lambda x, y, z: self.write_sequence(x.elements, y),
            DictionaryValue: lambda x, y, z: self.write_dictionary_value(x.elements, y),
        }
        self._omit_enclosing_object = omit_enclosing_object
        self._closing_delimiter = closing_delimiter if closing_delimiter else "\n"
        self._render_message = render_message
        self._render_message_template = render_message_template

    def format(self, log_event: LogEvent, output: StringWriteable):
        Guard.against_null(log_event)
        Guard.against_null(output)

        if not self._omit_enclosing_object:
            output.write("{")
        delim = ""
        delim = self.write_timestamp(log_event.timestamp, delim, output)
        delim = self.write_level(log_event.level, delim, output)
        if self._render_message_template:
            delim = self.write_message_template(log_event.message_template, delim, output)
        if self._render_message:
            message = log_event.render_message()
            delim = self.write_rendered_message(message, delim, output)

        if log_event.exception is not None:
            delim = self.write_exception(log_event.exception, delim, output)

        if len(log_event.properties) > 0:
            self.write_properties(log_event.properties, output)
        if not self._omit_enclosing_object:
            output.write("}")
            output.write(self._closing_delimiter)

    def write_literal(self, value, output: StringWriteable, force_quotation: bool = False):
        if value is None:
            output.write("null")
            return

        value_type = type(value)
        if value_type in self._literal_writers:
            self._literal_writers[value_type](value, output, force_quotation)
            return
        self.write_literal_value(value, output)

    def write_json_property(self, name: str, value, preceding_delimiter: str, output: StringWriteable) -> str:
        output.write(f'{preceding_delimiter}"{name}":')
        self.write_literal(value, output)
        return ","

    def write_timestamp(self, timestamp: datetime, preceding_delimiter: str, output: StringWriteable) -> str:
        return self.write_json_property("Timestamp", timestamp, preceding_delimiter, output)

    def write_level(self, level: LogEventLevel, preceding_delimiter: str, output: StringWriteable) -> str:
        return self.write_json_property("Level", level, preceding_delimiter, output)

    def write_message_template(self, template: MessageTemplate, delim: str, output: StringWriteable):
        return self.write_json_property("message_template", template, delim, output)

    def write_rendered_message(self, template: str, delim: str, output: StringWriteable):
        return self.write_json_property("rendered_message", template, delim, output)

    def write_exception(self, exception: Exception, delim: str, output: StringWriteable):
        return self.write_json_property("Exception", exception, delim, output)

    def write_properties(self, properties: dict[str, LogEventPropertyValue], output: StringWriteable):
        output.write(',"properties":{')
        self.write_properties_values(properties, output)
        output.write("}")

    def write_properties_values(self, properties: dict[str, LogEventPropertyValue], output: StringWriteable):
        preceding_delimiter = ""
        for key in properties.keys():
            preceding_delimiter = self.write_json_property(key, properties[key], preceding_delimiter, output)

    def write_literal_value(self, value: object, output: StringWriteable):
        self.write_string(str(value), output)

    @staticmethod
    def write_string(value: str, output: StringWriteable):
        JsonValueFormatter.write_quoted_json_string(value, output)

    def write_to_string(self, value, output: StringWriteable, quote=False):
        if quote:
            output.write('"')
        self.write_literal(str(value), output)
        if quote:
            output.write('"')

    @staticmethod
    def write_datetime(value: datetime, output: StringWriteable):
        output.write(f'"{value.isoformat()}"')

    def write_list(self, value: list, output: StringWriteable):
        output.write("[")
        for i in range(len(value)):
            if i > 0:
                output.write(",")
            self.write_literal(value[i], output)
        output.write("]")

    def write_dict(self, value: dict, output: StringWriteable):
        output.write("{")
        keys = list(value.keys())
        delim = ""
        for i in range(len(keys)):
            key = keys[i]
            delim = self.write_json_property(key, value[key], delim, output)
        output.write("}")

    def write_sequence(self, elements: list, output: StringWriteable):
        output.write("[")
        delim = ""
        for elm in elements:
            output.write(delim)
            delim = ","
            self.write_literal(elm, output, True)
        output.write("]")

    def write_dictionary_value(self, elements: list[tuple[ScalarValue, LogEventPropertyValue]], output: StringWriteable):
        output.write("{")
        delim = ""
        for elm in elements:
            output.write(delim)
            delim = ","
            self.write_literal(elm[0], output)
            output.write(":")
            self.write_literal(elm[1], output)
        output.write("}")
