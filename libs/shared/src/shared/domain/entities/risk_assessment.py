from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from shared.domain.enums import RiskLevel


@dataclass
class RiskAssessment:
    client_id: UUID
    document_id: UUID
    risk_score: Decimal  # 0.0000 – 1.0000
    model_version: str
    features_used: list[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    assessed_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def risk_level(self) -> RiskLevel:
        score = float(self.risk_score)
        if score < 0.3:
            return RiskLevel.LOW
        if score < 0.6:
            return RiskLevel.MEDIUM
        if score < 0.85:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    @property
    def is_critical(self) -> bool:
        return self.risk_level == RiskLevel.CRITICAL

    def to_report_dict(self) -> dict[str, object]:
        return {
            "id": str(self.id),
            "client_id": str(self.client_id),
            "risk_score": float(self.risk_score),
            "risk_level": self.risk_level,
            "model_version": self.model_version,
            "assessed_at": self.assessed_at.isoformat(),
        }
