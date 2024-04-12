from pyserilog_sinks_elasticsearch.sinks.enums import AutoRegisterTemplateVersion
from pyserilog_sinks_elasticsearch.sinks.options import ElasticsearchSinkOptions


def get_template(options: ElasticsearchSinkOptions
                 , discovered_major_version: int,
                 settings: dict[str, str],
                 template_matching_string: str,
                 version: AutoRegisterTemplateVersion = AutoRegisterTemplateVersion.ESv7) -> dict[str, str]:
    match version:
        case AutoRegisterTemplateVersion.ESv8:
            return get_template_esv8(options, discovered_major_version, settings, template_matching_string)
        case AutoRegisterTemplateVersion.ESv7:
            return get_template_esv7(options, discovered_major_version, settings, template_matching_string)
        case AutoRegisterTemplateVersion.ESv6:
            return get_template_esv6(discovered_major_version, settings, template_matching_string)
    raise ValueError("Invalid version")


def get_template_esv8(options: ElasticsearchSinkOptions
                      , discovered_major_version: int,
                      settings: dict[str, str],
                      template_matching_string: str):
    templateV7 = get_template_esv7(options, discovered_major_version, settings, template_matching_string)

    return {
        "index_patterns": templateV7["index_patterns"],
        "template": {
            "settings": templateV7["settings"],
            "mappings": templateV7["mappings"],
            "aliases": templateV7["aliases"],
        }
    }


def get_template_esv7(options: ElasticsearchSinkOptions
                      , discovered_major_version: int,
                      settings: dict[str, str],
                      template_matching_string: str) -> dict:
    mappings = {
        "dynamic_templates": [
            {
                "numerics_in_fields": {
                    "path_match": "fields\.[\d+]$",
                    "match_pattern": "regex",
                    "mapping": {
                        "type": "text",
                        "index": True,
                        "norms": False,
                    }
                }
            }, {
                "string_fields": {
                    "match": "*",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "text",
                        "norms": False,
                        "index": True,
                        "fields": {
                            "raw": {
                                "type": "keyword",
                                "index": True,
                                "ignore_above": 256
                            }
                        }
                    }
                }
            }
        ],
        "properties": {
            "message": {"type": "text", "index": True},
        }
    }

    mappings = {"_doc": mappings} if discovered_major_version == 6 else mappings

    aliases = dict()
    if options.index_aliases is not None:
        for alias in options.index_aliases:
            aliases[alias] = dict()

    return {
        "settings": settings,
        "mappings": mappings,
        "aliases": aliases,
        "index_patterns": template_matching_string,
    }


def get_template_esv6(discovered_major_version: int,
                      settings: dict[str, str],
                      template_matching_string: str) -> dict:
    mappings = {
        "dynamic_templates": [
            {
                "numerics_in_fields": {
                    "path_match": "fields\.[\d+]$",
                    "match_pattern": "regex",
                    "mapping": {
                        "type": "text",
                        "index": True,
                        "norms": False,
                    }
                }
            }, {
                "string_fields": {
                    "match": "*",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "text",
                        "norms": False,
                        "index": True,
                        "fields": {
                            "raw": {
                                "type": "keyword",
                                "index": True,
                                "ignore_above": 256
                            }
                        }
                    }
                }
            }
        ],
        "properties": {
            "message": {"type": "text", "index": True},
        }
    }

    mappings = {"_doc": mappings} if discovered_major_version == 7 else {"_default_": mappings}

    return {
        "settings": settings,
        "mappings": mappings,
        "index_patterns": template_matching_string,
    }
