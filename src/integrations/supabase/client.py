from __future__ import annotations

from supabase import Client, create_client

from src.config import Settings


def create_supabase_client(
    settings: Settings | None = None,
) -> Client:
    if settings is None:
        settings = Settings.from_env()

    settings.validate()

    return create_client(
        settings.supabase_url,
        settings.supabase_key,
    )