from collections.abc import Callable
from datetime import datetime
from enum import Enum
from typing import Optional

from pyserilog.events.log_event import LogEvent
from pyserilog.formatting import ITextFormatter

from pyserilog_formating_elasticsearch.conf.config import Config
from pyserilog_sinks_elasticsearch.sinks.enums import AutoRegisterTemplateVersion


class RegisterTemplateRecovery(Enum):
    INDEX_ANYWAY = 1
    """
    Ignore the issue and keep indexing. This is the default option.
    """
    INDEX_TO_DEAD_LETTER_INDEX = 4
    """
    When the template cannot be registered, move the events to the deadLetter index instead.
    """
    FAIL_SINK = 8
    """
    When the template cannot be registered, throw an exception and fail the sink.
    """


class ElasticsearchSinkOptions:
    def __init__(self):
        self.auto_register_template: bool = False
        """
            When set to true the sink will register an index template for the logs in elasticsearch.
            This template is optimized to deal with serilog events
        """
        self.number_of_shards: Optional[int] = None
        """
            When using the `AutoRegisterTemplate` feature, this allows you to override the default number of shards.
            If not provided, this will default to the default number_of_shards configured in Elasticsearch.
        """
        self.overwrite_template: bool = False
        """
            When using the `AutoRegisterTemplate` feature, this allows you to overwrite the template in Elasticsearch if it already exists.
            Defaults to: `false`
        """
        self.template_name: str = "serilog-events-template"
        """
            When using the `AutoRegisterTemplate` feature this allows you to override the default template name.
            Defaults to: serilog-events-template
        """
        self.number_of_replicas: Optional[int] = None
        """
            When using the `AutoRegisterTemplate` feature, this allows you to override the default number of replicas.
            If not provided, this will default to the default number_of_replicas configured in Elasticsearch.
        """
        self.index_format: str = "logstash-{%Y.%m.%d}"
        """
            The index name formatter. A string.Format using the DateTimeOffset of the event is run over this string.
            defaults to "logstash-{%Y.%m.%d}"
            Needs to be lowercased.
        """
        self.dead_letter_index_name: str = "deadletter-{%Y.%m.%d}"
        """
            Optionally set this value to the name of the index that should be used when the template cannot be written to ES.
            defaults to "deadLetter-{%Y.%m.%d}"
        """
        self.type_name: Optional[str] = None
        """
            The default elasticsearch type name to use for the log events. Defaults to: `None`.
        """

        self.auto_register_template_version: Optional[AutoRegisterTemplateVersion] = None
        """
        When using the `AutoRegisterTemplate` feature, this allows to set the Elasticsearch version. Depending on the
        version, a template will be selected. Defaults to 7.0.
        """

        self.batch_posting_limit: int = 50
        """
        The maximum number of events to post in a single batch. Defaults to: 50.
        """

        self.pipeline_name: str = ""
        """
        Name the Pipeline where log events are sent to sink. Please note that the Pipeline should be existing before the usage starts.
        """

        self.period: float = 2.0
        """
        The time to wait between checking for event batches. Defaults to 2.0 seconds.
        """

        self.queue_size_limit: Optional[int] = 100000
        """
        The maximum number of events that will be held in-memory while waiting to ship them to Elasticsearch.
        Beyond this limit, events will be dropped. The default is 100,000. Has no effect on durable log shipping.
        """
        self.batch_posting_limit: int = 50
        """
        The maximum number of events to post in a single batch. Defaults to: 50.
        """
        self.hosts: list[str] = ["http://localhost:8200"]
        """
        The elastic search hosts to send the logs to. Defaults to: ["http://localhost:8200"]
        """
        self.register_template_failure: RegisterTemplateRecovery = RegisterTemplateRecovery.INDEX_ANYWAY
        """
        Specifies the option on how to handle failures when writing the template to Elasticsearch.
        This is only applicable when using the AutoRegisterTemplate option.
        """

        self.custom_formatter: Optional[ITextFormatter] = None
        """
        Customizes the formatter used when converting log events into ElasticSearch documents. Please note that the formatter output must be valid JSON :)
        """
        self.formatter_config: Optional[Config] = None
        """
        Define configuration of the formatter.
        """

        self.detect_elasticsearch_version: bool = True
        """
        Instructs the sink to auto detect the running Elasticsearch version.\n
        This information is used to attempt to register an older or newer template and to decide which version of index-template API to use.
        """
        self.index_aliases: list[str] = []
        """
        Index aliases. Sets alias/aliases to an index in elasticsearch.
        If not provided, index aliases will be blank.
        """
        self.template_custom_settings: dict[str, str] = dict()
        """
        When using the `AutoRegisterTemplate` feature, this allows you to override the default template content.
        If not provided, a default template that is optimized to deal with Serilog events is used.
        """
        self.elasticsearch_transporter = None
        """
        Elastic Search client Just use for test purposes
        """
        self.inline_fields: bool = False
        """
        When true fields will be written at the root of the json document.
        """

        self.index_decider: Callable[[LogEvent, datetime], str] = None
        """
        Function to decide which index to write the LogEvent to, when using file see: BufferIndexDecider
        """
