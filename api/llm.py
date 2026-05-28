from __future__ import annotations

import logging
import os
import threading

import api  # noqa: F401 — ensures .env is loaded and sys.path is set
from huskyadvisor.models import AdvisingResult, StudentProfile

logger = logging.getLogger(__name__)

_client = None
_client_lock = threading.Lock()
GROQ_MODEL = "llama-3.3-70b-versatile"


def _decision_inputs(profile: StudentProfile, context: str) -> list[str]:
    inputs = [
        f"context={context}",
        f"major={profile.major}",
        f"standing={profile.class_standing}",
    ]
    if profile.completed_courses:
        inputs.append(f"completed_courses={len(profile.completed_courses)} provided")
    if profile.career_goals:
        inputs.append(f"career_goals={', '.join(profile.career_goals)}")
    if profile.target_companies:
        inputs.append(f"target_companies={', '.join(profile.target_companies)}")
    return inputs


def _with_ai_trace(
    profile: StudentProfile,
    result: AdvisingResult,
    context: str,
    *,
    llm_enhancement: str,
    llm_model: str | None = None,
) -> AdvisingResult:
    return result.model_copy(
        update={
            "ai_trace": result.ai_trace.model_copy(
                update={
                    "recommendation_engine": "profile-aware structured scoring with completed-course filtering and company/pathway weighting",
                    "llm_enhancement": llm_enhancement,
                    "llm_model": llm_model,
                    "data_ingestion": "curated UWB/company JSON datasets plus Crawl4AI raw-to-normalized refresh pipeline",
                    "retrieval_readiness": "normalized Crawl4AI exports can feed vector/retrieval documents for RAG-style advising",
                    "fallback_mode": False,
                    "decision_inputs": _decision_inputs(profile, context),
                }
            )
        }
    )


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
        return _with_ai_trace(
            profile,
            result,
            context,
            llm_enhancement="not configured; structured engine result returned",
        )

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
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        enhanced = AdvisingResult(
            title=result.title,
            summary=response.choices[0].message.content.strip(),
            recommendations=result.recommendations,
            evidence=result.evidence,
            cautions=result.cautions,
        )
        return _with_ai_trace(
            profile,
            enhanced,
            context,
            llm_enhancement="Groq Llama 3.3 personalized summary generated",
            llm_model=GROQ_MODEL,
        )
    except Exception:
        logger.exception("LLM enhance failed for context=%s (major redacted)", context)
        return _with_ai_trace(
            profile,
            result,
            context,
            llm_enhancement="attempted but failed; structured engine result returned",
            llm_model=GROQ_MODEL,
        )  # graceful fallback — never break the API
