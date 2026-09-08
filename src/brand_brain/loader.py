import json
from pathlib import Path

from jsonschema import Draft202012Validator


class BrandDNALoader:
    """
    Carga y valida Brand DNA contra el contrato canónico.

    Responsabilidad única:
    - cargar el schema;
    - cargar un Brand DNA;
    - validar el Brand DNA.

    No modifica el Brand DNA.
    No calcula relevancia.
    No genera contenido.
    """

    def __init__(self, schema_path: str | Path):
        self.schema_path = Path(schema_path)

        with self.schema_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            self.schema = json.load(file)

        self.validator = Draft202012Validator(
            self.schema
        )

    def load(
        self,
        brand_dna_path: str | Path,
    ) -> dict:
        path = Path(brand_dna_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            brand_dna = json.load(file)

        self.validate(brand_dna)

        return brand_dna

    def validate(
        self,
        brand_dna: dict,
    ) -> None:
        errors = sorted(
            self.validator.iter_errors(brand_dna),
            key=lambda error: list(error.path),
        )

        if errors:
            messages = []

            for error in errors:
                location = ".".join(
                    str(part)
                    for part in error.path
                )

                if not location:
                    location = "<root>"

                messages.append(
                    f"{location}: {error.message}"
                )

            raise ValueError(
                "Invalid Brand DNA:\n"
                + "\n".join(messages)
            )