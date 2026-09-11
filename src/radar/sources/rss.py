from __future__ import annotations

from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from src.radar.config import RSSFeedConfig


class RSSSource:
    """
    Adaptador RSS V0.

    Responsabilidad única:
    - descargar un feed RSS;
    - convertir sus entradas a raw_signals compatibles con RadarV0.

    No crea RadarSignal directamente.
    No evalúa relevancia.
    No utiliza Brand Brain.
    """

    def __init__(
        self,
        feed_config: RSSFeedConfig,
        timeout: int = 15,
    ):
        if not feed_config.url:
            raise ValueError("feed_url must not be empty.")

        if timeout <= 0:
            raise ValueError("timeout must be greater than zero.")

        self.feed_config = feed_config
        self.timeout = timeout

    def fetch(self) -> list[dict]:
        """
        Descarga el feed y devuelve señales crudas normalizadas.
        """

        request = Request(
            self.feed_config.url,
            headers={
                "User-Agent": "KCE-Creator-OS/0.1",
            },
        )

        with urlopen(request, timeout=self.timeout) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        signals = []

        for item in self._find_items(root):
            signal = self._parse_item(item)

            signal["language"] = self.feed_config.language
            signal["evidence"] = {
                "feed_url": self.feed_config.url,
            }

            signals.append(signal)

        return signals

    @staticmethod
    def _find_items(root: ET.Element) -> list[ET.Element]:
        """
        Encuentra entradas RSS <item>.

        V0 soporta RSS clásico.
        Atom se incorporará posteriormente si hace falta.
        """

        return root.findall(".//item")

    @staticmethod
    def _parse_item(item: ET.Element) -> dict:
        """
        Convierte un <item> RSS a raw_signal.

        Se mantiene como método estático por compatibilidad
        con el contrato histórico de RSSSource.
        """

        title = RSSSource._text(item, "title")
        summary = RSSSource._text(item, "description")

        categories = RSSSource._parse_keywords(
            RSSSource._text(item, "category")
        )

        return {
            "source_type": "rss",
            "platform": "rss",
            "url": RSSSource._text(item, "link"),
            "author": RSSSource._text(item, "author"),
            "published_at": RSSSource._text(item, "pubDate"),
            "title": title,
            "summary": summary,
            "keywords": categories,
            "topics": categories,
            "language": "es",
            "evidence": {},
            "niches": [],
            "relevance_reason": "",
            "confidence": 0.5,
        }

    @staticmethod
    def _text(
        item: ET.Element,
        tag: str,
    ) -> str:
        """
        Obtiene el texto de un elemento RSS.
        """

        element = item.find(tag)

        if element is None or element.text is None:
            return ""

        return element.text.strip()

    @staticmethod
    def _parse_keywords(value: str) -> list[str]:
        if not value:
            return []

        return [
            keyword.strip()
            for keyword in value.split(",")
            if keyword.strip()
        ]


class RSSRadarSource(RSSSource):
    """
    Adaptador RSS compatible con el contrato RadarSource.

    Permite construir una fuente directamente con una URL,
    mientras RSSSource mantiene la interfaz histórica basada
    en RSSFeedConfig.
    """

    def __init__(
        self,
        feed_url: str,
        timeout: int = 15,
        language: str = "en",
    ) -> None:
        if not feed_url:
            raise ValueError("feed_url must not be empty.")

        super().__init__(
            feed_config=RSSFeedConfig(
                name="RSS Feed",
                url=feed_url,
                language=language,
                enabled=True,
            ),
            timeout=timeout,
        )

    @property
    def feed_url(self) -> str:
        return self.feed_config.url