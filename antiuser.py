import discord
from discord.ext import commands
import asyncio

# ================== config ==================

TOKEN = "BOT_TOKEN"

TARGET_USER_ID = THE_USER_iD

SOUND_FILE = "sound.mp3"

FFMPEG_PATH = r"THE_PATH_FFMPEG"

# ==============================================


intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ connect as {bot.user}")


@bot.event
async def on_voice_state_update(member, before, after):

    # Ελέγχουμε αν είναι ο σωστός χρήστης
    if member.id != TARGET_USER_ID:
        return

    # Αν μόλις μπήκε σε voice
    if before.channel is None and after.channel is not None:

        channel = after.channel

        try:
            print("🎯 the target join in voice!")

            # Connect bot
            vc = await channel.connect()

            # Φόρτωση ήχου
            source = discord.FFmpegPCMAudio(
                SOUND_FILE,
                executable=FFMPEG_PATH
            )

            # play
            vc.play(source)

            # Περιμένει να τελειώσει
            while vc.is_playing():
                await asyncio.sleep(1)

            # Kick από voice
            await member.move_to(None)

            print("❌ the target is disconnect!")

            # Φεύγει το bot
            await vc.disconnect()

        except Exception as e:
            print("⚠️ error:", e)


bot.run(TOKEN)
