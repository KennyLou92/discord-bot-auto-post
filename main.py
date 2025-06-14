import discord
from discord.ext import commands
import requests
from datetime import datetime
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

SENT_LOG_PATH = "sent_images.txt"

# 確保 sent_images.txt 存在
if not os.path.exists(SENT_LOG_PATH):
    open(SENT_LOG_PATH, 'w').close()

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def get_next_version():
    now = datetime.now()
    year = now.year + (now.month // 12)
    month = now.month % 12 + 1
    return f"{year}{month:02d}"

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
    with open(SENT_LOG_PATH, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_sent_log(sent_urls):
    with open(SENT_LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(sent_urls)))

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    await send_images()

async def send_images():
    version = get_next_version()
    urls = generate_urls(version)
    sent = load_sent_log()
    new_urls = [url for url in urls if url not in sent and requests.get(url).status_code == 200]

    if not new_urls:
        print("ℹ️ No new images to send.")
        return

    channel = bot.get_channel(CHANNEL_ID)
    thread = await channel.create_thread(name=f"Update {version}", type=discord.ChannelType.public_thread)

    for i in range(0, len(new_urls), 10):
        embed_objs = []
        group = new_urls[i:i+10]
        for url in group:
            embed = discord.Embed()
            embed.set_image(url=url)
            embed_objs.append(embed)

        try:
            await thread.send(embeds=embed_objs)
            sent.update(group)
        except Exception as e:
            print(f"❌ Failed to send image group: {e}")

    save_sent_log(sent)

bot.run(TOKEN)
