# Notion 데이터베이스 저장

요약된 영상 정보를 Notion 데이터베이스에 저장한다.

## 사전 조건

`/summarize` 실행 결과(영상별 요약 데이터)가 필요합니다.

## 설정 확인

`config/channels.json`의 `notion.database_id`를 읽으세요.
`database_id`가 "PLACEHOLDER"이면 이 단계를 건너뛰고 "Notion 미설정 - config/channels.json에서 notion.database_id를 설정하세요"라고 보고하세요.

## 저장

MCP 도구 `notion-create-pages`로 각 영상별 페이지를 생성합니다:

- properties:
  - 제목: 영상 제목
  - 채널: 채널명
  - URL: 영상 URL
  - 날짜: 현재 날짜
- content: 요약 내용 (마크다운 형식)

각 영상별로 개별 페이지를 생성하세요.
저장 결과(성공/실패)를 보고하세요.
