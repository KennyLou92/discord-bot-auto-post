import discord
import requests
from datetime import datetime
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

def get_next_version():
    now = datetime.now()
    year = now.year + (now.month // 12)
    month = now.month % 12 + 1
    return f"{year}{month:02d}"  # e.g., 202506

def generate_urls(version):
    base = f"https://game-lgtmtmg.line-scdn.net/COMMON/G{version}/images/"
    paths = [
        "event_banner/info_main_tw.png",
        "event/main_header_tw.png",
        "event_banner/info_score_tw.png",
        "event_banner/heartsale_tw.png",
        "event_banner/itemsale_tw.png",
        "event_banner/info_bnr_boxbonus_tw.png",
        "event_banner/index_doubleup_2_tw.png",
        "box/box01_l_tw.png",
        "box/box02_l_tw.png",
        "box/box03_z_tw.png",
        "box/list_01_l_tw.png",
        "box/list_02_l_tw.png",
        "box/list_03_l_tw.png",
        "box/list_04_l_tw.png",
        "box/list_05_l_tw.png",
        "select/select01_head_tw.png",       
        "select/select01_list_tw.png",
        "select/select02_head_tw.png",
        "select/select02_list_tw.png",
        "select/select03_head_tw.png",
        "select/select03_list_tw.png",
        "pick/pick01_img_tw.png",
        "pick/pick01_limit_tw.png",
        "pick/pick02_img_tw.png",
        "pick/pick02_limit_tw.png",
        "boxbonus/boxbonus_tw.png",
        "event/score_header_tw.png",
        "raffle/raffle_header_tw.png",
        "event/sticker_header_tw.png",
        "event/scratch_header_tw.png",
        "bingo/bingo_header_tw.png",
    ]
    return [base + path for path in paths]

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user.name}")
    await send_images()
    await client.close()  # ⛔ 這是關鍵：執行完後結束 bot.run()

async def send_images():
    version = get_next_version()
    thread_name = f"{version}"
    urls = generate_urls(version)

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("❌ Channel not found. Check CHANNEL_ID.")
        return

    existing_threads = list(channel.threads)

    # 加入 archived threads
    archived_threads = []
    async for thread in channel.archived_threads(limit=50):
        archived_threads.append(thread)

    existing_threads += archived_threads

    for t in existing_threads:
        if t.name == thread_name:
            print(f"🛑 Thread '{thread_name}' already exists (even archived). Skipping creation.")
            return

    valid_urls = [url for url in urls if requests.get(url).status_code == 200]

    if not valid_urls:
        print("ℹ️ No valid image URLs found.")
        return

    thread = await channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)

    for i in range(0, len(valid_urls), 10):
        embeds = []
        for url in valid_urls[i:i+10]:
            embed = discord.Embed()
            embed.set_image(url=url)
            embeds.append(embed)
        await thread.send(embeds=embeds)

client.run(TOKEN)
