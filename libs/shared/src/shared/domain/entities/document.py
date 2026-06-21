from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from shared.domain.enums import DocumentStatus, DocumentType
from shared.utils.datetime_utils import _utcnow


@dataclass
class Document:
    id: UUID = field(default_factory=uuid4)
    client_id: UUID | None = None
    uploaded_by: UUID | None = None
    filename: str | None = None
    doc_type: DocumentType | None = None
    status: DocumentStatus = DocumentStatus.UPLOADED
    page_count: int | None = None
    word_count: int | None = None
    extracted_text: str | None = None
    error_message: str | None = None
    storage_path: str | None = None
    file_size_bytes: int | None = None
    uploaded_at: datetime = field(default_factory=_utcnow)
    parsed_at: datetime | None = None

    """ Domain Behaviors """

    def mark_parsing(self) -> None:
        if self.status != DocumentStatus.UPLOADED:
            raise ValueError(f"Cannot start parsing - document in status: {self.status!r}")
        self.status = DocumentStatus.PARSING

    def mark_parsed(self, page_count: int, word_count: int, text: str) -> None:
        if self.status != DocumentStatus.PARSING:
            raise ValueError(f"Expected PARSING state, got: {self.status!r}")
        self.status = DocumentStatus.PARSED
        self.page_count = page_count
        self.word_count = word_count
        self.extracted_text = text
        self.parsed_at = _utcnow()

    def mark_failed(self, error: str) -> None:
        self.status = DocumentStatus.FAILED
        self.error_message = error

    def archive(self) -> None:
        if self.status not in {DocumentStatus.PARSED, DocumentStatus.FAILED}:
            raise ValueError("Can only archive PARSED or FAILED documents")
        self.status = DocumentStatus.ARCHIVED

    @property
    def is_ready_for_ai(self) -> bool:
        return self.status == DocumentStatus.PARSED and self.extracted_text is not None

    @property
    def size_mb(self) -> float:
        if self.file_size_bytes is None:
            raise ValueError("No File Exists.")
        else:
            return round(self.file_size_bytes / (1024 * 1024), 2)
