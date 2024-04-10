from dataclasses import dataclass
from typing import Optional

from elasticsearch import Elasticsearch


@dataclass
class Version:
    major: int
    minor: int
    patch: int


class ElasticsearchVersionManger:

    def __init__(self, detect_version: bool, client: Elasticsearch):
        self._detect_version = detect_version
        self._client = client
        self._detected_version: Optional[Version] = None
        self._detection_attempt = False
        self._default_version = Version(7, 16, 0)

    @property
    def effective_version(self) -> Version:
        if self._detected_version is not None:
            return self._detected_version

        if self._detect_version is False or self._detection_attempt is True:
            return self._default_version

        self._detected_version = self._discover_cluster_version()
        return self._detected_version if self._detected_version else self._default_version

    def _discover_cluster_version(self) -> Optional[Version]:
        try:
            info = self._client.info()
            version: str = info["version"]["number"]
            parts = version.split(".")
            return Version(int(parts[0]), int(parts[1]), int(parts[2]))
        except Exception as e:
            print(e)
            return None
        finally:
            self._detection_attempt = True
