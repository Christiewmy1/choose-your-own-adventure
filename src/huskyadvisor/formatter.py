from __future__ import annotations

from huskyadvisor.models import AdvisingResult


def format_result(result: AdvisingResult) -> str:
    lines = [result.title, "", result.summary, ""]

    if result.recommendations:
        lines.append("Recommendations:")
        for item in result.recommendations:
            lines.append(f"- {item}")
        lines.append("")

    if result.evidence:
        lines.append("Why these suggestions:")
        for item in result.evidence:
            lines.append(f"- {item}")
        lines.append("")

    if result.cautions:
        lines.append("Things to keep in mind:")
        for item in result.cautions:
            lines.append(f"- {item}")

    return "\n".join(lines).strip()
