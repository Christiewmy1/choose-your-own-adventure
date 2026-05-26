from __future__ import annotations

import logging
import os
import threading

import api  # noqa: F401 — ensures .env is loaded and sys.path is set
from huskyadvisor.models import AdvisingResult, StudentProfile

logger = logging.getLogger(__name__)

_client = None
_client_lock = threading.Lock()


def _get_client():
    global _client
    if _client is not None:
        return _client
    with _client_lock:
        if _client is not None:
            return _client
        key = os.environ.get("GROQ_API_KEY", "")
        if not key:
            return None
        try:
            from groq import AsyncGroq
            _client = AsyncGroq(api_key=key)
        except ImportError:
            logger.error("groq package is not installed; LLM enhancement disabled")
            return None
    return _client


async def enhance(profile: StudentProfile, result: AdvisingResult, context: str) -> AdvisingResult:
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
        response = await client.chat.completions.create(
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
        logger.exception("LLM enhance failed for context=%s (major redacted)", context)
        return result  # graceful fallback — never break the API
