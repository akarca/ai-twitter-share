import logging

import tweepy

logger = logging.getLogger(__name__)


def post_thread(
    tweets,
    url=None,
    api_key=None,
    api_secret=None,
    access_token=None,
    access_secret=None,
):
    """Post a list of tweets as a Twitter/X thread.

    Args:
        tweets: List of tweet text strings. Must have at least 2 items.
        url: Optional URL appended to the last tweet.
        api_key: Twitter API consumer key.
        api_secret: Twitter API consumer secret.
        access_token: Twitter access token.
        access_secret: Twitter access token secret.

    Returns:
        ``True`` on success, ``False`` on failure.
    """
    if not tweets or len(tweets) < 2:
        logger.error("At least 2 tweets required for a thread")
        return False

    if not all([api_key, api_secret, access_token, access_secret]):
        logger.error("Twitter credentials are incomplete")
        return False

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )

        thread_tweets = list(tweets)
        if url:
            thread_tweets[-1] = f"{thread_tweets[-1]}\n\n{url}"

        prev_tweet_id = None
        for i, tweet_text in enumerate(thread_tweets):
            resp = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=prev_tweet_id,
            )
            prev_tweet_id = resp.data["id"]
            logger.info(
                "Tweet %d/%d sent: %s", i + 1, len(thread_tweets), tweet_text[:60]
            )

        logger.info("Thread shared to Twitter (%d tweets)", len(thread_tweets))
        return True

    except Exception as e:
        logger.error("Twitter share failed: %s", e)
        return False


def post_single_tweet(
    text,
    url=None,
    api_key=None,
    api_secret=None,
    access_token=None,
    access_secret=None,
):
    """Post a single tweet.

    Args:
        text: Tweet text.
        url: Optional URL appended to the tweet.
        api_key: Twitter API consumer key.
        api_secret: Twitter API consumer secret.
        access_token: Twitter access token.
        access_secret: Twitter access token secret.

    Returns:
        ``True`` on success, ``False`` on failure.
    """
    if not all([api_key, api_secret, access_token, access_secret]):
        logger.error("Twitter credentials are incomplete")
        return False

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )

        tweet_text = f"{text}\n\n{url}" if url else text
        client.create_tweet(text=tweet_text)
        logger.info("Shared to Twitter: %s", tweet_text[:80])
        return True

    except Exception as e:
        logger.error("Twitter share failed: %s", e)
        return False
