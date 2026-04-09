"""영상 필터링 스크립트 - 키워드, 기간, 중복 기준으로 필터링."""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.state import load_state, is_processed

CONFIG_PATH = Path(__file__).parent.parent / "config" / "channels.json"


def load_config(config_path=CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_iso_datetime(text):
    """ISO 8601 날짜 문자열을 datetime으로 변환. RSS 피드의 published 태그용."""
    if not text:
        return None
    try:
        # '2025-04-09T12:00:00+00:00' 형태
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def get_channel_config(channel_name, config):
    """채널 이름으로 채널 설정을 찾는다."""
    for ch in config.get("channels", []):
        if ch["name"] == channel_name:
            return ch
    return None


def filter_videos(videos, config):
    """모든 필터 조건을 적용하여 영상을 필터링한다."""
    state = load_state()
    filter_cfg = config.get("filter", {})
    exclude_keywords = [kw.lower() for kw in filter_cfg.get("exclude_keywords", [])]
    max_age_hours = filter_cfg.get("max_age_hours", 24)

    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    filtered = []

    for video in videos:
        video_id = video.get("video_id", "")
        title = video.get("title", "")
        title_lower = title.lower()
        channel_name = video.get("channel_name", "")

        # 1. 이미 처리된 영상 스킵
        if is_processed(video_id, state):
            continue

        # 2. 제외 키워드 체크
        if any(kw in title_lower for kw in exclude_keywords):
            continue

        # 3. 게시 시간 체크 (max_age_hours 이내)
        published_time = parse_iso_datetime(video.get("published", ""))
        if published_time and published_time < cutoff_time:
            continue

        # 4. 채널별 키워드 매칭
        ch_config = get_channel_config(channel_name, config)
        if ch_config:
            keywords = ch_config.get("keywords", [])
            if keywords:  # 키워드가 설정된 경우에만 필터링
                if not any(kw.lower() in title_lower for kw in keywords):
                    continue
            # keywords가 빈 배열이면 전체 수집 (증시각도기TV)

        filtered.append(video)

    return filtered


def main():
    videos = json.load(sys.stdin)
    config = load_config()
    result = filter_videos(videos, config)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
