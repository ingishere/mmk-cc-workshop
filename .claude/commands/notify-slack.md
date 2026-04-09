# Slack 알림 전송

요약된 영상 정보를 Slack 채널로 전송한다.

## 사전 조건

`/summarize` 실행 결과(영상별 요약 데이터)가 필요합니다.

## 설정 확인

`config/channels.json`의 `slack.channel_id`를 읽으세요.
`channel_id`가 "PLACEHOLDER"이면 이 단계를 건너뛰고 "Slack 미설정 - config/channels.json에서 slack.channel_id를 설정하세요"라고 보고하세요.

## 전송

MCP 도구 `slack_send_message`로 전송하세요.

메시지 포맷:
```
📈 주식 유튜브 모니터링 리포트 (YYYY-MM-DD HH:MM)

━━━━━━━━━━━━━━━━━━━━
[채널명] 영상 제목
🔗 영상 URL
━━━━━━━━━━━━━━━━━━━━
• 핵심 내용 요약 1
• 핵심 내용 요약 2
• 핵심 내용 요약 3
📊 종목/시장: 삼성전자, 코스피, S&P500 ...
📉 전망: 강세/약세/중립

(영상별로 반복)
```

메시지가 4000자를 초과하면 영상 단위로 분할하여 여러 메시지로 전송하세요.
