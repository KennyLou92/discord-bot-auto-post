import discord
from discord.ext import commands
import asyncio
import requests
from datetime import datetime
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# 用來記錄已發送過的圖片URL
SENT_LOG_PATH = "sent_images.txt"

# 若紀錄檔不存在，先建立一個空的
if not os.path.exists(SENT_LOG_PATH):
    with open(SENT_LOG_PATH, "w", encoding="utf-8") as f:
        pass

# Discord Bot intents 設定
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_current_version():
    now = datetime.now()
    return f"{now.year}{now.month:02d}" # e.g., 202506

def generate_urls(version):
    base = f"https://game-lgtmtmg.line-scdn.net/COMMON/G{version}/images/"
    paths = [
        "event_banner/info_main_tw.png",
        "event/main_header_tw.png",
        "box/list_01_l_tw.png",
        "box/list_02_l_tw.png",
        "box/list_03_l_tw.png",
        "box/list_04_l_tw.png",
        "box/list_05_l_tw.png",
        "event_banner/info_score_tw.png",
        "select/select01_list_tw.png",
        "select/select02_list_tw.png",
        "select/select03_list_tw.png",
        "select/select03_head_tw.png",
        "pick/pick01_limit_tw.png",
        "pick/pick02_limit_tw.png",
        "select/select01_head_tw.png",
        "select/select02_head_tw.png",
        "select/select03_head_tw.png",
        "pick/pick01_img_tw.png",
        "pick/pick02_img_tw.png",
        "box/box01_l_tw.png",
        "box/box02_l_tw.png",
        "box/box03_z_tw.png",
        "event_banner/heartsale_tw.png",
        "event_banner/itemsale_tw.png",
        "event_banner/info_bnr_boxbonus_tw.png",
        "boxbonus/boxbonus_tw.png",
        "event/score_header_tw.png",
        "raffle/raffle_header_tw.png",
        "event/sticker_header_tw.png",
        "event/scratch_header_tw.png",
        "bingo/bingo_header_tw.png",
        "event_banner/index_doubleup_2_tw.png"
    ]
    return [base + path for path in paths]

def load_sent_log():
    if os.path.exists(SENT_LOG_PATH):
        with open(SENT_LOG_PATH, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f)
    return set()

def save_sent_log(sent_urls):
    with open(SENT_LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sent_urls))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await send_images()
    await bot.close()  # 關閉 bot

async def send_images():
    version = get_current_version()
    urls = generate_urls(version)
    sent = load_sent_log()
    new_urls = [url for url in urls if url not in sent and requests.get(url).status_code == 200]

    if not new_urls:
        print("No new images to send.")
        return

    channel = bot.get_channel(CHANNEL_ID)
    thread = await channel.create_thread(name=f"Update {version}", type=discord.ChannelType.public_thread)

    for i in range(0, len(new_urls), 10):
        embed_objs = []
        for url in new_urls[i:i+10]:
            embed = discord.Embed()
            embed.set_image(url=url)
            embed_objs.append(embed)

        await thread.send(embeds=embed_objs)

    # 記錄已發送的 URL
    sent.update(new_urls)
    save_sent_log(sent)

bot.run(TOKEN)
