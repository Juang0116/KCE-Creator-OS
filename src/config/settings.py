from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            supabase_url=os.getenv("SUPABASE_URL", "").strip(),
            supabase_key=os.getenv("SUPABASE_KEY", "").strip(),
        )

    def validate(self) -> None:
        missing: list[str] = []

        if not self.supabase_url:
            missing.append("SUPABASE_URL")

        if not self.supabase_key:
            missing.append("SUPABASE_KEY")

        if missing:
            raise ValueError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )