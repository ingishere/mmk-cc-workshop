"""YouTube 채널 RSS 피드에서 최신 영상 목록을 수집하는 스크립트."""

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

CONFIG_PATH = Path(__file__).parent.parent / "config" / "channels.json"

# YouTube RSS Atom 네임스페이스
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

RSS_URL_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def load_config(config_path=CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_channel_videos(channel_id, channel_name, limit=10):
    """단일 채널의 RSS 피드에서 최신 영상을 가져온다."""
    url = RSS_URL_TEMPLATE.format(channel_id=channel_id)
    videos = []

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] {channel_name} RSS 피드 요청 실패: {e}", file=sys.stderr)
        return videos

    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as e:
        print(f"[ERROR] {channel_name} RSS XML 파싱 실패: {e}", file=sys.stderr)
        return videos

    entries = root.findall("atom:entry", NS)
    for entry in entries[:limit]:
        video_id_el = entry.find("yt:videoId", NS)
        title_el = entry.find("atom:title", NS)
        published_el = entry.find("atom:published", NS)

        if video_id_el is None:
            continue

        video_id = video_id_el.text
        title = title_el.text if title_el is not None else ""
        published = published_el.text if published_el is not None else ""

        videos.append({
            "video_id": video_id,
            "title": title,
            "channel_name": channel_name,
            "channel_id": channel_id,
            "published": published,
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })

    return videos


def fetch_all_channels(config):
    """설정된 모든 활성 채널에서 영상을 수집한다."""
    all_videos = []
    limit = config.get("processing", {}).get("videos_per_channel", 10)

    for ch in config.get("channels", []):
        if not ch.get("enabled", True):
            continue
        name = ch["name"]
        channel_id = ch["channel_id"]
        print(f"[INFO] {name} 채널 수집 중...", file=sys.stderr)
        videos = fetch_channel_videos(channel_id, name, limit=limit)
        print(f"[INFO] {name}: {len(videos)}개 영상 수집", file=sys.stderr)
        all_videos.extend(videos)

    return all_videos


def main():
    config = load_config()
    videos = fetch_all_channels(config)
    print(json.dumps(videos, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
