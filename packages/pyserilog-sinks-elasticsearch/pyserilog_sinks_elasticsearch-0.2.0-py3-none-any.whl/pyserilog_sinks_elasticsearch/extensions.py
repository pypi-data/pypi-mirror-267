from datetime import datetime
from typing import Optional, Callable

from pyserilog import LoggerConfiguration
from pyserilog.configuration.logger_sink_configuration import LoggerSinkConfiguration
from pyserilog.core.logging_level_switch import LoggingLevelSwitch
from pyserilog.events.level_alias import LevelAlias
from pyserilog.events.log_event import LogEvent
from pyserilog.events.log_event_level import LogEventLevel
from pyserilog.formatting import ITextFormatter

from pyserilog_sinks_elasticsearch.sinks.elasticsearch_sink import ElasticsearchSink
from pyserilog_sinks_elasticsearch.sinks.enums import AutoRegisterTemplateVersion
from pyserilog_sinks_elasticsearch.sinks.options import ElasticsearchSinkOptions, RegisterTemplateRecovery
from pyserilog_formating_elasticsearch.conf.config import Config as FormatterConfig


def elasticsearch(logger_sink_configuration: LoggerSinkConfiguration,
                  hosts: list[str],
                  auto_register_template: bool = False,
                  number_of_shards: Optional[int] = None,
                  number_of_replicas: Optional[int] = None,
                  level_switch: Optional[LoggingLevelSwitch] = None,
                  overwrite_template: bool = False,
                  template_name: Optional[str] = None,
                  index_format: Optional[str] = None,
                  batch_posting_limit: int = 50,
                  period: float = 2.0,
                  queue_size_limit: Optional[int] = 100000,
                  custom_formatter: Optional[ITextFormatter] = None,
                  formatter_config: Optional[FormatterConfig] = None,
                  index_decider: Callable[[LogEvent, datetime], str] = None,
                  register_template_failure: RegisterTemplateRecovery = RegisterTemplateRecovery.INDEX_ANYWAY,
                  auto_register_template_version: Optional[AutoRegisterTemplateVersion] = None,
                  restricted_to_minimum_level: LogEventLevel = LevelAlias.minimum
                  ) -> LoggerConfiguration:
    options = ElasticsearchSinkOptions()
    options.hosts = hosts
    options.auto_register_template = auto_register_template
    options.number_of_shards = number_of_shards
    options.number_of_replicas = number_of_replicas
    options.overwrite_template = overwrite_template
    options.auto_register_template_version = auto_register_template_version
    options.batch_posting_limit = batch_posting_limit
    options.period = period
    options.register_template_failure = register_template_failure,
    options.queue_size_limit = queue_size_limit
    options.custom_formatter = custom_formatter
    options.formatter_config = formatter_config if formatter_config else FormatterConfig()
    options.index_decider = index_decider
    if template_name is not None:
        options.template_name = template_name
    if index_format:
        options.index_format = index_format

    sink = ElasticsearchSink(options)

    return logger_sink_configuration.sink(sink, restricted_to_minimum_level, level_switch)
