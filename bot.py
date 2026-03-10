import discord
from discord.ext import commands
import random

TOKEN = "TOKEN"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

channels = {}


@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")


def get_channel_data(channel_id):
    if channel_id not in channels:
        channels[channel_id] = {
            "counter": 0,
            "targets": [],
            "mode": None
        }
    return channels[channel_id]


@bot.command()
async def start(ctx, *nums):

    data = get_channel_data(ctx.channel.id)

    data["counter"] = 0
    data["targets"] = []

    # !start
    if len(nums) == 0:
        data["mode"] = "count"
        await ctx.send("安価カウント開始")
        return

    # !start 20 30 40
    data["mode"] = "target"

    for n in nums:
        try:
            data["targets"].append(int(n))
        except:
            pass

    data["targets"].sort()

    await ctx.send(f"安価予約 {data['targets']}")


@bot.command()
async def stop(ctx):

    data = get_channel_data(ctx.channel.id)

    data["mode"] = None
    data["counter"] = 0
    data["targets"] = []

    await ctx.send("安価停止")


@bot.command()
async def now(ctx):

    data = get_channel_data(ctx.channel.id)

    await ctx.send(f"現在レス番号 >>{data['counter']}")


@bot.command()
async def random(ctx, num: int):

    data = get_channel_data(ctx.channel.id)

    data["counter"] = 0
    data["targets"] = [random.randint(1, num)]
    data["mode"] = "target"

    await ctx.send(f"ランダム安価 >>{data['targets'][0]}")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    data = get_channel_data(message.channel.id)

    if data["mode"] is None:
        await bot.process_commands(message)
        return

    data["counter"] += 1

    if data["mode"] == "count":
        await message.channel.send(f">>{data['counter']} {message.content}")

    elif data["mode"] == "target":

        if data["counter"] in data["targets"]:

            await message.channel.send(
                f">>{data['counter']} {message.content}"
            )

            data["targets"].remove(data["counter"])

            if len(data["targets"]) == 0:
                data["mode"] = None
                data["counter"] = 0

    await bot.process_commands(message)


bot.run(TOKEN)
