# ai-twitter-share

Claude AI ile tweet thread oluştur, Twitter/X'te paylaş.

## Kurulum

```bash
pip install git+https://github.com/akarca/ai-twitter-share
```

## Kullanım

### Tweet Thread Oluştur (Claude AI)

```python
from ai_twitter_share import generate_tweet_thread

tweets = generate_tweet_thread(
    title="Blog başlığı",
    summary="Kısa özet",
    content="Blog içeriği...",         # opsiyonel
    lang="tr",                          # "tr" veya "en"
    claude_api_key="sk-ant-...",
    claude_model="claude-sonnet-4-20250514",  # opsiyonel
    system_prompt=None,                 # opsiyonel, custom prompt
)
# Dönen değer: ["tweet 1", "tweet 2", "tweet 3", "tweet 4"] veya None
```

### Twitter'da Thread Paylaş

```python
from ai_twitter_share import post_thread

post_thread(
    tweets=["tweet 1", "tweet 2", "tweet 3", "tweet 4"],
    url="https://example.com/blog",   # son tweet'e eklenir
    api_key="...",
    api_secret="...",
    access_token="...",
    access_secret="...",
)
```

### Tek Tweet Paylaş

```python
from ai_twitter_share import post_single_tweet

post_single_tweet(
    text="Tweet metni",
    url="https://example.com",
    api_key="...",
    api_secret="...",
    access_token="...",
    access_secret="...",
)
```

### Tek Adımda Oluştur + Paylaş

```python
from ai_twitter_share import generate_and_post

generate_and_post(
    title="Blog başlığı",
    summary="Özet",
    url="https://example.com/blog",
    lang="tr",
    claude_api_key="sk-ant-...",
    twitter_api_key="...",
    twitter_api_secret="...",
    twitter_access_token="...",
    twitter_access_secret="...",
)
```

### Custom Prompt

```python
from ai_twitter_share import generate_tweet_thread

tweets = generate_tweet_thread(
    title="...",
    summary="...",
    lang="tr",
    claude_api_key="...",
    system_prompt="Sen bir spor editörüsün. 4 tweet'lik thread yaz...",
)
```

### Mevcut Prompt'ları Göster

```python
from ai_twitter_share import get_prompt

print(get_prompt("tr"))
print(get_prompt("en"))
```

## API

| Fonksiyon | Açıklama | Dönen Değer |
|-----------|----------|-------------|
| `generate_tweet_thread()` | Claude ile tweet thread oluşturur | `list[str]` veya `None` |
| `post_thread()` | Tweet listesini thread olarak paylaşır | `bool` |
| `post_single_tweet()` | Tek tweet paylaşır | `bool` |
| `generate_and_post()` | Oluştur + paylaş (tek adım) | `bool` |
| `get_prompt(lang)` | Dil bazlı system prompt döner | `str` |

## Gereksinimler

- Python >= 3.10
- `anthropic` — Claude API
- `tweepy` — Twitter API
