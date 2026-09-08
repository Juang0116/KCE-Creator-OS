import json

import pytest

from src.brand_brain.loader import BrandDNALoader


def make_valid_brand_dna():
    return {
        "schema_version": "1.0.0",
        "brand_id": "brand_test",
        "created_at": "2026-09-08T00:00:00+00:00",
        "updated_at": "2026-09-08T00:00:00+00:00",
        "status": "active",
        "version": 1,
        "identity": {
            "name": "Test Brand",
            "mission": "Test mission",
            "vision": "Test vision",
            "values": ["quality"],
            "value_proposition": "Test value",
            "positioning": "Test positioning",
        },
        "market": {
            "category": "technology",
            "competitors": [],
            "differentiators": [
                "clear educational content",
            ],
        },
        "audience": {
            "target": "Creators",
            "interests": ["AI"],
            "problems": ["complex technology"],
            "desires": ["learn"],
            "knowledge_level": "mixed",
            "geography": [],
            "languages": ["en"],
        },
        "personality": {
            "archetype": "Sage",
            "tone": ["clear"],
            "voice": "professional",
            "attitude": ["helpful"],
        },
        "content": {
            "pillars": ["technology"],
            "formats": ["video"],
            "topics": ["AI"],
            "storytelling": "educational",
        },
        "channels_community": {
            "primary_platforms": ["YouTube"],
            "content_repurposing": "shorts",
            "engagement_strategy": "community",
        },
        "visual": {
            "style": "modern",
            "colors": ["blue"],
            "characters": [],
            "animation": "minimal",
        },
        "rules": {
            "do": ["educate"],
            "dont": ["mislead"],
            "sensitive_topics": [],
        },
        "business": {
            "goals": ["growth"],
            "monetization": ["ads"],
            "kpis": ["views"],
        },
    }


def test_loader_loads_valid_brand_dna(tmp_path):
    schema_path = "schemas/brand_dna.schema.json"

    brand_dna_path = tmp_path / "brand_dna.json"

    brand_dna = make_valid_brand_dna()

    brand_dna_path.write_text(
        json.dumps(brand_dna),
        encoding="utf-8",
    )

    loader = BrandDNALoader(schema_path)

    loaded = loader.load(brand_dna_path)

    assert loaded == brand_dna


def test_loader_rejects_invalid_brand_dna(tmp_path):
    schema_path = "schemas/brand_dna.schema.json"

    brand_dna_path = tmp_path / "invalid_brand_dna.json"

    brand_dna = make_valid_brand_dna()

    del brand_dna["identity"]

    brand_dna_path.write_text(
        json.dumps(brand_dna),
        encoding="utf-8",
    )

    loader = BrandDNALoader(schema_path)

    with pytest.raises(ValueError, match="identity"):
        loader.load(brand_dna_path)


def test_loader_validate_accepts_valid_brand_dna():
    loader = BrandDNALoader(
        "schemas/brand_dna.schema.json"
    )

    brand_dna = make_valid_brand_dna()

    loader.validate(brand_dna)


def test_loader_validate_rejects_invalid_brand_dna():
    loader = BrandDNALoader(
        "schemas/brand_dna.schema.json"
    )

    brand_dna = make_valid_brand_dna()

    brand_dna["version"] = 0

    with pytest.raises(ValueError, match="version"):
        loader.validate(brand_dna)