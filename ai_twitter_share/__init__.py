from .generator import generate_tweet_thread
from .poster import post_single_tweet, post_thread
from .prompts import get_prompt

__all__ = [
    "generate_tweet_thread",
    "post_thread",
    "post_single_tweet",
    "get_prompt",
    "generate_and_post",
]


def generate_and_post(
    title,
    summary="",
    url=None,
    content=None,
    lang="tr",
    claude_api_key=None,
    claude_model="claude-sonnet-4-20250514",
    system_prompt=None,
    twitter_api_key=None,
    twitter_api_secret=None,
    twitter_access_token=None,
    twitter_access_secret=None,
):
    """Generate a tweet thread with Claude and post it to Twitter.

    Returns:
        ``True`` on success, ``False`` on failure.
    """
    tweets = generate_tweet_thread(
        title=title,
        summary=summary,
        content=content,
        lang=lang,
        claude_api_key=claude_api_key,
        claude_model=claude_model,
        system_prompt=system_prompt,
    )
    if not tweets:
        return False

    return post_thread(
        tweets=tweets,
        url=url,
        api_key=twitter_api_key,
        api_secret=twitter_api_secret,
        access_token=twitter_access_token,
        access_secret=twitter_access_secret,
    )
