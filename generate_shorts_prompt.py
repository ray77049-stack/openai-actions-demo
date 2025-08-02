import json
import os
import urllib.request


def fetch_hot_topics():
    """Fetch hot topics from Google Trends; fall back to a static list on failure."""
    url = (
        "https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=-120&geo=TW&ns=15"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read().decode("utf-8")
        # The API prepends )]}'\n to avoid XSSI. Strip it then parse JSON.
        payload = json.loads(data.split("\n", 1)[1])
        topics = [
            item["title"]["query"]
            for item in payload["default"]["trendingSearchesDays"][0]["trendingSearches"]
        ]
        return topics[:3]
    except Exception:
        return [
            "AI-generated K-pop dance craze",
            "Olympics breaking world records",
            "Viral cat vs. robot vacuum",
        ]


def generate_prompt(topic: str) -> str:
    """Generate a YouTube Shorts prompt for a given topic using OpenAI's API."""
    prompt = f"""
You are an expert social media video creator.
Generate a creative, viral YouTube Shorts video prompt about the trending topic: "{topic}".

Include:
- A catchy English title
- A short description of the video concept
- A detailed scene-by-scene breakdown (0-2s, 2-4s, 4-6s, 6-8s)
- Add a fun or witty dialogue or subtitle

Style: Engaging, trendy, cinematic.
    """

    body = {
        "model": "gpt-4o-mini",
        "input": [
            {"role": "system", "content": "You are an expert social media video creator."},
            {"role": "user", "content": prompt},
        ],
    }

    api_key = os.getenv("OPENAI_API_KEY", "")
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        return result.get("output_text", "")
    except Exception as exc:
        return f"Error generating prompt for topic '{topic}': {exc}"


def main():
    topics = fetch_hot_topics()
    for topic in topics:
        print(f"\n=== Trending Topic: {topic} ===")
        print(generate_prompt(topic))
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
