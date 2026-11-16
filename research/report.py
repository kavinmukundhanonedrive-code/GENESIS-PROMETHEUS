from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SourceReference:
    title: str
    url: str
    summary: str = ""
    verified: bool = False


@dataclass
class ResearchFinding:
    fact: str
    interpretation: str = ""
    confidence: float = 0.0
    references: List[str] = field(default_factory=list)


@dataclass
class ResearchReport:
    query: str
    findings: List[ResearchFinding] = field(default_factory=list)
    references: List[SourceReference] = field(default_factory=list)
    summary: str = ""

    def add_reference(self, reference: SourceReference) -> None:
        self.references.append(reference)

    def add_finding(self, fact: str, interpretation: str = "", confidence: float = 0.0, references: Optional[List[str]] = None) -> None:
        self.findings.append(
            ResearchFinding(
                fact=fact,
                interpretation=interpretation,
                confidence=float(confidence),
                references=list(references or []),
            )
        )

    def to_markdown(self) -> str:
        lines: List[str] = [f"# Research report: {self.query}", "", "## Summary", self.summary or "No summary provided.", "", "## Findings"]
        for index, finding in enumerate(self.findings, start=1):
            lines.append(f"### {index}. Fact")
            lines.append(f"- Fact: {finding.fact}")
            if finding.interpretation:
                lines.append(f"- Interpretation: {finding.interpretation}")
            lines.append(f"- Confidence: {finding.confidence:.2f}")
            if finding.references:
                lines.append(f"- References: {', '.join(finding.references)}")
            lines.append("")
        lines.extend(["## Sources"])
        if not self.references:
            lines.append("- No source references captured.")
        for ref in self.references:
            lines.append(f"- [{ref.title}]({ref.url}) — {'verified' if ref.verified else 'unverified'}: {ref.summary or 'No summary'}")
        return "\n".join(lines)
