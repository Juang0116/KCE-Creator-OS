from datetime import datetime, timezone
from uuid import uuid4

from .models import (
    AssetPlan,
    AssetPlanProcessing,
    AssetPlanSource,
    AssetPlanTarget,
    AssetRequirement,
)


class AssetEngineV0:
    """
    Deterministic V0 asset planning engine.

    Converts a Storyboard into a structured inventory of
    assets required for production.

    V0 does not generate, download, or retrieve real assets.
    """

    def generate(self, storyboard) -> AssetPlan:
        asset_plan_id = f"asset_plan_{uuid4().hex[:12]}"
        created_at = datetime.now(timezone.utc).isoformat()

        source = AssetPlanSource(
            storyboard_id=storyboard.storyboard_id,
            script_id=storyboard.source.script_id,
            idea_id=storyboard.source.idea_id,
            opportunity_id=storyboard.source.opportunity_id,
            signal_id=storyboard.source.signal_id,
        )

        target = AssetPlanTarget(
            brand_id=storyboard.target.brand_id,
            channel=storyboard.target.channel,
            platform=storyboard.target.platform,
        )

        assets = []

        for scene in storyboard.scenes:
            for index, visual_asset in enumerate(
                scene.visual_assets,
                start=1,
            ):
                asset_id = f"asset_{uuid4().hex[:12]}"

                asset_type = self._infer_asset_type(visual_asset)

                assets.append(
                    AssetRequirement(
                        asset_id=asset_id,
                        scene_id=scene.scene_id,
                        asset_type=asset_type,
                        description=visual_asset,
                        purpose=(
                            f"Support visual storytelling for "
                            f"{scene.section_id}."
                        ),
                        source_strategy=self._infer_source_strategy(
                            asset_type
                        ),
                        priority="medium",
                        status="needed",
                        required=True,
                    )
                )

        if not assets:
            assets.append(
                AssetRequirement(
                    asset_id=f"asset_{uuid4().hex[:12]}",
                    scene_id=storyboard.scenes[0].scene_id,
                    asset_type="other",
                    description="Supporting visual asset",
                    purpose="Provide visual support for the scene.",
                    source_strategy="create",
                    priority="medium",
                    status="needed",
                    required=True,
                )
            )

        processing = AssetPlanProcessing(
            status="draft",
            confidence=storyboard.processing.confidence,
            processed_at=None,
        )

        return AssetPlan(
            schema_version="1.0",
            asset_plan_id=asset_plan_id,
            created_at=created_at,
            asset_plan_version="1",
            source=source,
            target=target,
            assets=assets,
            processing=processing,
        )

    @staticmethod
    def _infer_asset_type(asset_name: str) -> str:
        value = asset_name.lower()

        if "screenshot" in value or "captura" in value:
            return "screenshot"

        if "video" in value or "clip" in value:
            return "video"

        if "background" in value or "fondo" in value:
            return "background"

        if "icon" in value or "icono" in value:
            return "icon"

        if "graphic" in value or "gráfico" in value:
            return "graphic"

        if "audio" in value or "sound" in value:
            return "audio"

        if "text" in value or "texto" in value:
            return "text"

        return "image"

    @staticmethod
    def _infer_source_strategy(asset_type: str) -> str:
        strategies = {
            "image": "retrieve",
            "video": "retrieve",
            "graphic": "create",
            "screenshot": "capture",
            "background": "generate",
            "icon": "retrieve",
            "text": "create",
            "audio": "generate",
            "other": "create",
        }

        return strategies.get(asset_type, "create")