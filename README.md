<p align="center">
<img height="256" src="img.svg">
</p>

<h1 align="center">GAS</h1>

<p align="center">GameWorks Automation System<br/>GAS is a Discord automated chat-bot enhances efficiency of your work.</p>

---
## Features

- Notion에서 새 업무를 생성할 경우 Discord 채널을 통해 알림을 받습니다.
- 업무의 상태를 변경할 경우 Discord 채널을 통해 알림을 받습니다.
- 업무에 인원을 배정할 경우 Discord 채널을 통해 알림을 받습니다.
- 업무의 마감일 전에 Discord 채널을 통해 리마인드 메시지를 받습니다.

## Configuration

GAS를 사용하기 위해서는 다음과 같은 설정이 필요합니다.

### Notion

1. Notion API 키를 발급받습니다.
2. Notion에서 사용할 데이터베이스를 생성합니다.
3. 데이터베이스의 ID를 확인합니다.
4. `secrets.py`의 `NOTION_TOKEN`과 `DATABASE_ID`에 각각 발급받은 API 키와 데이터베이스 ID를 입력합니다.
5. 데이터베이스의 속성 이름을 확인합니다.
6. `config.py`의 `TITLE`, `DATE`, `STATS`, `ASSIGNEE`에 각각 데이터베이스의 속성 이름을 입력합니다.

### Discord

1. Discord 봇을 생성합니다.
2. 봇의 토큰을 확인합니다.
3. `secrets.py`의 `DISCORD_TOKEN`에 봇의 토큰을 입력합니다.
4. 봇을 원하는 서버에 초대합니다.
5. 봇이 접근할 수 있는 채널의 ID를 확인합니다.
6. `config.py`의 `CHANNEL_ID`에 봇이 접근할 채널의 ID를 입력합니다.

```
