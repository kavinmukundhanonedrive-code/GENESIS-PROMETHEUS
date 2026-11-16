from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from research.report import ResearchReport, SourceReference


@dataclass
class ResearchMode:
    """Structured research context that separates verified facts from interpretation."""

    working_report: Optional[ResearchReport] = None

    def start_report(self, query: str) -> ResearchReport:
        self.working_report = ResearchReport(query=query)
        return self.working_report

    def add_reference(self, title: str, url: str, summary: str = "", verified: bool = False) -> SourceReference:
        if self.working_report is None:
            raise ValueError("A research report must be started before adding references.")
        reference = SourceReference(title=title, url=url, summary=summary, verified=verified)
        self.working_report.add_reference(reference)
        return reference

    def add_finding(self, fact: str, interpretation: str = "", confidence: float = 0.0, references: Optional[List[str]] = None) -> None:
        if self.working_report is None:
            raise ValueError("A research report must be started before adding findings.")
        self.working_report.add_finding(fact=fact, interpretation=interpretation, confidence=confidence, references=references)

    def finalize(self, summary: str) -> ResearchReport:
        if self.working_report is None:
            raise ValueError("No report is active.")
        self.working_report.summary = summary
        return self.working_report

    def to_markdown(self) -> str:
        if self.working_report is None:
            raise ValueError("No report is active.")
        return self.working_report.to_markdown()
