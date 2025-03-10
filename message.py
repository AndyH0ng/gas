import discord, notion
from discord.ext import commands, tasks
from const import secrets, config, strings

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    check_status_changes.start()
    check_new_task.start()
    check_new_assignee.start()

# 업무 상태 변경 감지
previous_status = {}
@tasks.loop(seconds=config.REFRESH_INTERVAL)
async def check_status_changes():
    pages = notion.get_pages()
    for page in pages:
        page_id = page['id']
        title = page['properties'][config.TITLE]['title'][0]['text']['content']
        status = page['properties'][config.STATS]['status']['name']

        if page_id in previous_status:
            if previous_status[page_id] != status:
                previous_status[page_id] = status
                channel = client.get_channel(int(secrets.CHANNEL_ID_1))
                await channel.send(strings.MODIFIED_STATS.format(title, status))
        else:
            previous_status[page_id] = status

# 새로운 업무 감지
previous_pages = {page['id'] for page in notion.get_pages()}
@tasks.loop(seconds=config.REFRESH_INTERVAL)
async def check_new_task():
    pages = notion.get_pages()
    current_page_ids = {page['id'] for page in pages}
    new_page_ids = current_page_ids - previous_pages

    for page in pages:
        page_id = page['id']
        if page_id in new_page_ids:
            title = page['properties'][config.TITLE]['title'][0]['text']['content'] if page['properties'][config.TITLE]['title'] else None
            channel = client.get_channel(int(secrets.CHANNEL_ID_1))
            await channel.send(strings.NEW_TASK_ADDED.format(title))

    previous_pages.update(new_page_ids)

# 새로운 인원 배정 감지
previous_assignees = {}
@tasks.loop(seconds=config.REFRESH_INTERVAL)
async def check_new_assignee():
    pages = notion.get_pages()
    for page in pages:
        page_id = page['id']
        title = page['properties'][config.TITLE]['title'][0]['text']['content'] if page['properties'][config.TITLE]['title'] else None
        current_assignees = {person['name'] for person in page['properties'][config.ASSIGNEE]['people']}

        if page_id in previous_assignees:
            new_assignees = current_assignees - previous_assignees[page_id]
            if new_assignees:
                channel = client.get_channel(int(secrets.CHANNEL_ID_1))
                for assignee in new_assignees:
                    await channel.send(strings.NEW_PERSON.format(title, assignee))
            previous_assignees[page_id] = current_assignees
        else:
            previous_assignees[page_id] = current_assignees

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$list'):
        pages = notion.get_pages()
        for page in pages:
            page_id = page['id']
            title = page['properties'][config.TITLE]['title'][0]['text']['content']
            date_start = page['properties'][config.DATE]['date']['start']
            date_end = page['properties'][config.DATE]['date']['end']
            status = page['properties'][config.STATS]['status']['name']
            people = page['properties'][config.ASSIGNEE]['people'][0]['name'] if page['properties'][config.ASSIGNEE]['people'] else None
            await message.channel.send(f'제목: {title}, 날짜: {date_start} ~ {date_end}, 정보: {status}, 사람: {people}')

client.run(secrets.DISCORD_TOKEN)