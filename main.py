import discord
import aiohttp
import asyncio
import os
from datetime import datetime
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # 文字頻道 ID

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

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await send_images()
    await bot.close()

async def send_images():
    version = get_next_version()
    urls = generate_urls(version)

    valid_urls = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        valid_urls.append(url)
            except:
                continue

    if not valid_urls:
        print("❌ No valid image URLs found.")
        return

    channel = bot.get_channel(CHANNEL_ID)
    thread = await channel.create_thread(
        name=f"G{version}",
        type=discord.ChannelType.public_thread
    )

    # 發送圖片 embed（可分批）
    for i, url in enumerate(valid_urls):
        embed = discord.Embed()
        if i == 0:
            embed.title = f"Version G{version}"
        embed.set_image(url=url)
        await thread.send(embed=embed)
        await asyncio.sleep(1)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
