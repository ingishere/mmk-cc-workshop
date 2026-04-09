# YouTube 채널 최신 영상 수집

설정된 YouTube 채널들의 RSS 피드에서 최신 영상 목록을 수집한다.

## 실행

```bash
cd /home/user/mmk-cc-workshop && python3 src/fetch_videos.py
```

결과를 JSON으로 파싱하여 보고하세요:
- 채널별 수집된 영상 수
- 각 영상의 제목, URL, 게시 시간

에러가 발생하면 stderr 메시지를 확인하고 보고하세요.
수집된 영상이 0개이면 "채널 접속 실패"를 보고하고 종료하세요.
