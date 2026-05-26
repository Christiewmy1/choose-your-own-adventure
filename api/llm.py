from __future__ import annotations

import os

import api  # noqa: F401 — ensures .env is loaded and sys.path is set
from huskyadvisor.models import AdvisingResult, StudentProfile

_client = None


def _get_client():
    global _client
    if _client is None:
        key = os.environ.get("GROQ_API_KEY", "")
        if not key:
            return None
        from groq import Groq
        _client = Groq(api_key=key)
    return _client


def enhance(profile: StudentProfile, result: AdvisingResult, context: str) -> AdvisingResult:
    """Replace the rule-based summary with an LLM-generated one.
    Falls back to the original result if the key is missing or the call fails.
    """
    client = _get_client()
    if client is None:
        return result

    prompt = f"""You are HuskyAdvisor, a friendly academic advisor for UW Bothell students.

Student:
- Major: {profile.major}
- Standing: {profile.class_standing}
- Career goals: {", ".join(profile.career_goals) or "not specified"}
- Target companies: {", ".join(profile.target_companies) or "none"}

The advising engine produced these {context} recommendations:
{chr(10).join(f"- {r}" for r in result.recommendations)}

Write 2-3 sentences: a warm, specific summary explaining why these fit this student's path.
Be encouraging. Reference their major and goals directly. Do not list the items again."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return AdvisingResult(
            title=result.title,
            summary=response.choices[0].message.content.strip(),
            recommendations=result.recommendations,
            evidence=result.evidence,
            cautions=result.cautions,
        )
    except Exception:
        return result  # graceful fallback — never break the API
