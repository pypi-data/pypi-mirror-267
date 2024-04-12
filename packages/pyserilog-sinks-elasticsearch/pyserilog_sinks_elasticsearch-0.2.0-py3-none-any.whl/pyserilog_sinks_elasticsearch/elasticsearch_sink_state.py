from datetime import datetime

from elastic_transport import HeadApiResponse
from elasticsearch import Elasticsearch
from pyserilog import Guard
import re

from pyserilog.events.log_event import LogEvent
from pyserilog.formatting import ITextFormatter

from pyserilog_formating_elasticsearch.elasticsearch_json_formatter import ElasticsearchJsonFormatter
from pyserilog_sinks_elasticsearch.sinks.elasticsearch_version_manager import ElasticsearchVersionManger
from pyserilog_sinks_elasticsearch.sinks.options import ElasticsearchSinkOptions, RegisterTemplateRecovery
from pyserilog_sinks_elasticsearch.sinks.enums import AutoRegisterTemplateVersion

INDEX_FORMAT_REGEX = re.compile('^(.*)\{(?P<date_pattern>(?:%.+)+)}(.*)$')


class ElasticsearchSinkState:

    @staticmethod
    def create(options: ElasticsearchSinkOptions) -> 'ElasticsearchSinkState':
        Guard.against_null(options)

        return ElasticsearchSinkState(options)

    def __init__(self, options: ElasticsearchSinkOptions):
        if options.index_format is None or len(options.index_format) == 0:
            raise ValueError("options.index_format must be a valid string")
        if options.template_name is None or len(options.template_name) == 0:
            raise ValueError("options.template_name must be a valid string")

        # Since TypeName is deprecated we shouldn't set it, if has been deliberately set to null.
        if options.type_name is not None and options.auto_register_template_version == AutoRegisterTemplateVersion.ESv7:
            options.type_name = "_doc"

        self._template_name = options.template_name
        self._template_match_string = INDEX_FORMAT_REGEX.sub(r'\1*\3', options.index_format)

        self._options = options

        self._client = Elasticsearch(
            hosts=options.hosts,
            _transport=options.elasticsearch_transporter
        )

        self._formatter = options.custom_formatter if options.custom_formatter \
            else self._create_default_formatter(options)

        date_pattern = INDEX_FORMAT_REGEX.match(options.index_format).group("date_pattern")

        def index_decider_func(x: LogEvent, timestamp: datetime):
            if date_pattern is not None:
                date_format = timestamp.strftime(date_pattern)
            else:
                date_format = timestamp.strftime("%Y.%m.%d")
            result = self._template_match_string.replace("*", date_format)
            return result.lower()

        self._index_decider = options.index_decider if options.index_decider else index_decider_func

        self._version_manager = ElasticsearchVersionManger(options.detect_elasticsearch_version, self._client)
        self._register_template_on_startup = options.auto_register_template
        self._template_registration_success = not self._register_template_on_startup

    @property
    def template_registration_success(self):
        return self._template_registration_success

    @property
    def client(self) -> Elasticsearch:
        return self._client

    def register_template_if_needed(self):
        if not self._register_template_on_startup:
            return
        try:
            if not self._options.overwrite_template:
                exist_response: HeadApiResponse = self._client.indices.exists_template(name=self._template_name)
                if exist_response:
                    self._template_registration_success = True
                    return
            data = self._get_template_data()
            result = self._client.indices.put_template(name=self._template_name, **data)
            if not result:
                if self._options.register_template_failure == RegisterTemplateRecovery.FAIL_SINK:
                    raise Exception("Failed to register template name {0}".format(self._template_name))
                self._template_registration_success = False
            else:
                self._template_registration_success = True

        except Exception as e:
            self._template_registration_success = False
            if self._options.register_template_failure == RegisterTemplateRecovery.FAIL_SINK:
                raise e

    def _get_template_data(self) -> dict:
        settings: dict[
            str, str] = self._options.template_custom_settings if self._options.template_custom_settings is not None else dict()
        settings["index.refresh_interval"] = "5s"
        if self._options.number_of_shards is not None:
            settings["number_of_shards"] = str(self._options.number_of_shards)
        if self._options.number_of_replicas is not None:
            settings["number_of_replicas"] = str(self._options.number_of_replicas)

        effective_template_version = self._get_effective_template_version()
        from pyserilog_sinks_elasticsearch.sinks.provider import get_template
        return get_template(self._options,
                            self._version_manager.effective_version.major,
                            settings,
                            self._template_match_string, effective_template_version)

    def _get_effective_template_version(self):
        if self._options.auto_register_template_version is not None:
            return self._options.auto_register_template_version
        if self._version_manager.effective_version.major >= 8:
            return AutoRegisterTemplateVersion.ESv8
        elif self._version_manager.effective_version.major == 7:
            return AutoRegisterTemplateVersion.ESv7
        elif self._version_manager.effective_version.major == 6:
            return AutoRegisterTemplateVersion.ESv6
        raise ValueError("Invalid version")

    @property
    def options(self):
        return self._options

    @property
    def formatter(self) -> ITextFormatter:
        return self._formatter

    @staticmethod
    def _create_default_formatter(options: ElasticsearchSinkOptions) -> ITextFormatter:
        return ElasticsearchJsonFormatter(
            closing_delimiter="",
            config=options.formatter_config,
            inline_fields=options.inline_fields
        )

    def get_index_for_event(self, event, timestamp):
        if not self._template_registration_success and self._options.register_template_failure == RegisterTemplateRecovery.INDEX_TO_DEAD_LETTER_INDEX:
            return self._options.dead_letter_index_name.format(timestamp)
        return self._index_decider(event, timestamp)
