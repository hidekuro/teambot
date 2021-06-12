# -*- coding: utf-8 -*-
import os
import random
import sys
from logging import INFO, Formatter, StreamHandler, getLogger
from logging.handlers import SYSLOG_UDP_PORT, SysLogHandler

import discord
from discord.enums import ChannelType
from discord.ext import commands

# Discord bot
bot = commands.Bot(command_prefix='*', description="shika bot")

# Logger
simpleFormatter = Formatter("[%(levelname)s] %(message)s")
consoleHandler = StreamHandler(sys.stdout)
consoleHandler.setFormatter(simpleFormatter)
syslogHandler = SysLogHandler(address=('localhost', SYSLOG_UDP_PORT))
syslogHandler.setFormatter(simpleFormatter)
LOGGER = getLogger(__file__)
LOGGER.setLevel(INFO)
LOGGER.addHandler(consoleHandler)
LOGGER.addHandler(syslogHandler)


def get_context_vc(ctx: commands.Context) -> discord.channel.VoiceChannel:
    u"""発言者がいるVCを取得する

    Args:
        ctx: コンテキストオブジェクト

    Returns:
        発言者がいるVCの VoiceChannel オブジェクト
    """
    author = ctx.message.author
    server = ctx.message.server  # type: discord.server.Server
    all_vc = list(c for c in server.channels if c.type == ChannelType.voice)
    return next(c for c in all_vc if author in c.voice_members)


def team_alloc(members: list, alloc_size: int) -> list:
    u"""指定の割り当てサイズに近い人数で均等にチーム分配する

    Args:
        members: 参加者リスト
        alloc_size: 1チーム当たりの人数

    Returns:
        均等に分配されたチームのリスト
    """
    total = len(members)

    if total % alloc_size == 0:
        # 割り切れる場合
        # チーム数＝人数 / 割り当てサイズ
        teams = total // alloc_size
    else:
        # 余る場合
        # チーム数＝人数 / 割り当てサイズ + 1
        teams = total // alloc_size + 1

    # 各チームの人数リスト
    sizes = [(total + i) // teams for i in range(teams)]

    # シャッフル
    random.shuffle(members)
    members_iter = iter(members)

    # 割り振り
    result = []
    for i, s in enumerate(sizes):
        team = []
        for _ in range(s):
            m = next(members_iter)
            team.append(m)
        result.append(team)

    return result


def team_to_string(teams) -> str:
    u"""チームのリストを表す2次元リストの文字列表現を取得する

    Args:
        teams: チームのリストを表す2次元リスト

    Returns:
        文字列表現
    """
    result = ""
    for i, t in enumerate(teams):
        members = ""
        for m in t:
            if members:
                members += ", "
            members += m.nick or m.name
        result += u"[Team {0}] {1}\n".format(i + 1, members)
    return result


async def proc_alloc_command(ctx: commands.Context, alloc_size: int):
    u"""チーム割り振りコマンドを処理し、返答する。

    Args:
        ctx: commands.Context オブジェクト
        alloc_size: 1チームあたりの人数
    """
    # 発言者のVCにいるメンバーリスト
    live_vc = get_context_vc(ctx)
    members = live_vc.voice_members

    # 簡易テスト用
    # members = list(m for m in ctx.message.server.members if m != bot.user)

    # チーム分け
    result = team_alloc(members, alloc_size)

    # 返答
    reply = team_to_string(result)
    await bot.say(reply)


@bot.event
async def on_ready():
    LOGGER.info("Logged in as {0.name}#{0.id}".format(bot.user))


@bot.command(pass_context=True)
async def duo(ctx: commands.Context):
    u"""1チームあたり2人に近くなるよう均等にチーム分けする
    """
    await proc_alloc_command(ctx, 2)


@bot.command(pass_context=True, aliases=["sq"])
async def squad(ctx: commands.Context):
    u"""1チームあたり4人に近くなるよう均等にチーム分けする
    """
    await proc_alloc_command(ctx, 4)


@bot.command(pass_context=True)
async def team(ctx: commands.Context, alloc_size: int):
    u"""指定人数に近くなるよう均等にチーム分けする
    """
    await proc_alloc_command(ctx, alloc_size)


@bot.command(pass_context=True)
async def dice(ctx: commands.Context, dimen: int = 6):
    u"""1から指定数値までのダイスを振る
    """
    num = random.randint(1, dimen)
    await bot.say("{0.mention} {1}".format(ctx.message.author, num))


def main():
    bot.run(os.environ.get("BOT_TOKEN"))


if __name__ == '__main__':
    main()
