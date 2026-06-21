from __future__ import annotations

from enum import StrEnum


class DocumentStatus(StrEnum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    FAILED = "failed"
    ARCHIVED = "archived"


class DocumentType(StrEnum):
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    PPTX = "pptx"


class UserRole(StrEnum):
    ANALYST = "analyst"
    RISK_MANAGER = "risk_manager"
    ADMIN = "admin"
    VIEWER = "viewer"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @classmethod
    def from_score(cls, score: float) -> RiskLevel:
        if score < 0.3:
            return cls.LOW
        if score < 0.6:
            return cls.MEDIUM
        if score < 0.85:
            return cls.HIGH
        return cls.CRITICAL


class PipelineStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
