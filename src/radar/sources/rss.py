from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


class RSSSource:
    """
    Adaptador V0.1 para obtener señales desde un feed RSS.

    Responsabilidad única:
    - descargar un feed RSS;
    - convertir sus entradas a raw_signals compatibles con RadarV0.

    No crea RadarSignal directamente.
    No evalúa relevancia.
    No utiliza Brand Brain.
    No calcula Opportunity Score.
    """

    def __init__(
        self,
        feed_url: str,
        timeout: int = 15,
    ):
        self.feed_url = feed_url
        self.timeout = timeout

    def fetch(self) -> list[dict]:
        """
        Descarga el feed y devuelve señales crudas normalizadas.
        """

        request = Request(
            self.feed_url,
            headers={
                "User-Agent": "KCE-Creator-OS/0.1",
            },
        )

        with urlopen(request, timeout=self.timeout) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        return [
            self._parse_item(item)
            for item in self._find_items(root)
        ]

    @staticmethod
    def _find_items(root: ET.Element) -> list[ET.Element]:
        """
        Encuentra entradas RSS <item>.

        V0.1 soporta RSS clásico.
        Atom se incorporará posteriormente si hace falta.
        """

        return root.findall(".//item")

    @staticmethod
    def _parse_item(item: ET.Element) -> dict:
        """
        Convierte un <item> RSS a raw_signal.
        """

        title = RSSSource._text(item, "title")
        summary = RSSSource._text(item, "description")

        return {
            "source_type": "rss",
            "platform": "rss",
            "url": RSSSource._text(item, "link"),
            "author": RSSSource._text(item, "author"),
            "published_at": RSSSource._text(item, "pubDate"),
            "title": title,
            "summary": summary,
            "keywords": [],
            "topics": [],
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
    ) -> str | None:
        """
        Obtiene el texto de un elemento RSS.
        """

        element = item.find(tag)

        if element is None or element.text is None:
            return None

        return element.text.strip()