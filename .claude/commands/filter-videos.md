# 영상 필터링

수집된 영상 목록에서 키워드, 게시 기간, 처리 이력을 기준으로 필터링한다.

## 사전 조건

`/fetch-videos` 실행 결과 JSON이 필요합니다.

## 실행

수집된 영상 JSON을 stdin으로 전달합니다:

```bash
cd /home/user/mmk-cc-workshop && echo '<수집된_영상_JSON>' | python3 src/filter_videos.py
```

## 필터 규칙 (`config/channels.json`)

1. 이미 처리된 영상 스킵 (`data/processed_videos.json` 참조)
2. 제외 키워드: shorts, #shorts, 라이브, LIVE
3. 게시 시간: max_age_hours(24시간) 이내
4. 채널별 키워드 매칭:
   - 한경글로벌마켓: 개장전요것만, 빈난새, 월스트리트나우, 김현석, 빈틈없이월가
   - 한국경제TV: 당잠사
   - 증시각도기TV: 전체 수집 (키워드 필터 없음)

필터링 결과가 빈 배열 `[]`이면 "새로운 영상이 없습니다"라고 보고하고 종료하세요.
