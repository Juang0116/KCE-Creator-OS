import json
from pathlib import Path
from xml.etree import ElementTree as ET

from jsonschema import Draft202012Validator

from src.radar import RadarV0
from src.radar.sources.rss import RSSSource


SAMPLE_RSS = """\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>KCE Test Feed</title>
        <item>
            <title>Nuevo avance en inteligencia artificial</title>
            <description>Una descripción de prueba.</description>
            <link>https://example.com/article</link>
            <author>Test Author</author>
            <pubDate>Tue, 08 Sep 2026 10:00:00 GMT</pubDate>
        </item>
    </channel>
</rss>
"""


def test_rss_source_parses_item(monkeypatch):
    class MockResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def read(self):
            return SAMPLE_RSS.encode("utf-8")

    def mock_urlopen(request, timeout):
        return MockResponse()

    monkeypatch.setattr(
        "src.radar.sources.rss.urlopen",
        mock_urlopen,
    )

    source = RSSSource(
        "https://example.com/feed.xml"
    )

    result = source.fetch()

    assert len(result) == 1

    signal = result[0]

    assert signal["source_type"] == "rss"
    assert signal["platform"] == "rss"
    assert signal["title"] == (
        "Nuevo avance en inteligencia artificial"
    )
    assert signal["summary"] == (
        "Una descripción de prueba."
    )
    assert signal["url"] == (
        "https://example.com/article"
    )
    assert signal["author"] == "Test Author"


def test_rss_source_output_is_compatible_with_radar():
    root = ET.fromstring(SAMPLE_RSS)
    item = root.find(".//item")

    signal = RSSSource._parse_item(item)

    required_fields = {
        "source_type",
        "platform",
        "title",
        "summary",
    }

    assert required_fields.issubset(signal.keys())


def test_rss_source_integrates_with_radar_and_schema(
    monkeypatch,
):
    class MockResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def read(self):
            return SAMPLE_RSS.encode("utf-8")

    def mock_urlopen(request, timeout):
        return MockResponse()

    monkeypatch.setattr(
        "src.radar.sources.rss.urlopen",
        mock_urlopen,
    )

    source = RSSSource(
        "https://example.com/feed.xml"
    )

    raw_signals = source.fetch()

    radar = RadarV0()
    signals = radar.collect(raw_signals)

    assert len(signals) == 1

    signal_data = signals[0].to_dict()

    schema_path = (
        Path(__file__).parent.parent
        / "schemas"
        / "radar_signal.schema.json"
    )

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = json.load(file)

    validator = Draft202012Validator(schema)

    errors = list(
        validator.iter_errors(signal_data)
    )

    assert not errors, "\n".join(
        error.message for error in errors
    )