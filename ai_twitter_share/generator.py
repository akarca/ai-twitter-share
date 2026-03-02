import json
import logging
import re

import anthropic

from .prompts import get_prompt

logger = logging.getLogger(__name__)


def _extract_tweet_text(item):
    """Extract text from a tweet item — may be a string or a dict."""
    if isinstance(item, dict):
        return (
            item.get("tweet") or item.get("text") or item.get("content") or ""
        ).strip()
    return str(item).strip()


def _parse_tweets(text):
    """Parse a JSON string into a list of tweet strings.

    Handles both plain arrays ``["t1", "t2"]`` and wrapped
    ``{"tweets": ["t1", "t2"]}`` formats, as well as dict items
    like ``{"tweet": "...", "characters": 215}``.

    Returns a list of cleaned tweet strings or *None* on failure.
    """

    def _clean(items):
        cleaned = []
        for t in items[:4]:
            t = _extract_tweet_text(t)
            t = re.sub(r"https?://\S+", "", t).strip()
            if t:
                cleaned.append(t)
        return cleaned if len(cleaned) >= 2 else None

    # Direct parse
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return _clean(data)
        if isinstance(data, dict):
            tweets = data.get("tweets", [])
            if isinstance(tweets, list):
                return _clean(tweets)
    except (json.JSONDecodeError, AttributeError):
        pass

    # Fallback: bracket extraction
    bracket_start = text.find("[")
    bracket_end = text.rfind("]")
    if bracket_start != -1 and bracket_end > bracket_start:
        try:
            tweets = json.loads(text[bracket_start : bracket_end + 1])
            if isinstance(tweets, list):
                return _clean(tweets)
        except json.JSONDecodeError:
            pass

    return None


def generate_tweet_thread(
    title,
    summary="",
    content=None,
    lang="tr",
    claude_api_key=None,
    claude_model="claude-sonnet-4-20250514",
    system_prompt=None,
    max_tokens=1024,
):
    """Generate a tweet thread using Claude AI.

    Args:
        title: Blog/article title.
        summary: Short summary text.
        content: Full content (first 2000 chars used). Optional.
        lang: Language code for prompt selection ("tr" or "en").
        claude_api_key: Anthropic API key. Required.
        claude_model: Claude model identifier.
        system_prompt: Custom system prompt. Overrides built-in prompts.
        max_tokens: Max tokens for Claude response.

    Returns:
        A list of tweet strings (typically 4), or *None* on failure.
    """
    if not claude_api_key:
        raise ValueError("claude_api_key is required")

    system = system_prompt or get_prompt(lang)

    content_snippet = ""
    if content:
        content_snippet = f"\nİçerik:\n{content[:2000]}"

    prompt = f"Başlık: {title}\nÖzet: {summary or ''}{content_snippet}"

    client = anthropic.Anthropic(api_key=claude_api_key)
    try:
        resp = client.messages.create(
            model=claude_model,
            max_tokens=max_tokens,
            system=system,
            messages=[
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": '["'},
            ],
        )
        text = '["' + resp.content[0].text.strip()
    except Exception as e:
        logger.error("Claude API call failed: %s", e)
        return None

    tweets = _parse_tweets(text)
    if tweets is None:
        logger.error(
            "Tweet array could not be extracted: %s", text[:300]
        )
    return tweets
