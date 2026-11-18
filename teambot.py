import itertools
import logging
import math
import os
import random
import sys
from collections.abc import Sequence

import discord
from discord import app_commands

LOGGER = logging.getLogger(__name__)


def team_alloc[T](members: Sequence[T], alloc_size: int) -> list[list[T]]:
    """指定の人数に近くなるよう均等にチーム分けする

    Args:
        members: 参加者
        alloc_size: 1 チームあたりの人数の上限

    Returns:
        チームごとの参加者のリスト
    """
    total = len(members)
    team_count = math.ceil(total / alloc_size)
    sizes = [(total + i) // team_count for i in range(team_count)]

    shuffled = list(members)
    random.shuffle(shuffled)
    unassigned = iter(shuffled)
    return [list(itertools.islice(unassigned, size)) for size in sizes]


def team_to_string(teams: Sequence[Sequence[discord.Member]]) -> str:
    """チーム分けの結果を返答用の文字列にする

    Args:
        teams: チームごとの参加者

    Returns:
        `[Team 1] a, b` の形の行をチームごとに並べた文字列
    """
    lines = []
    for i, team in enumerate(teams, start=1):
        names = ", ".join(
            discord.utils.escape_mentions(discord.utils.escape_markdown(m.display_name))
            for m in team
        )
        lines.append(f"[Team {i}] {names}")
    return "\n".join(lines)


async def reply_teams(interaction: discord.Interaction, alloc_size: int) -> None:
    """実行した人の VC にいるメンバーをチーム分けし、返答する

    Args:
        interaction: スラッシュコマンドの interaction
        alloc_size: 1 チームあたりの人数の上限
    """
    user = interaction.user
    voice = user.voice if isinstance(user, discord.Member) else None
    if voice is None or voice.channel is None:
        await interaction.response.send_message(
            "ボイスチャンネルに入ってから実行してください", ephemeral=True
        )
        return

    teams = team_alloc(voice.channel.members, alloc_size)
    await interaction.response.send_message(team_to_string(teams))


@app_commands.command()
@app_commands.guild_only()
async def duo(interaction: discord.Interaction) -> None:
    """1 チームあたり 2 人に近くなるよう均等にチーム分けする"""
    await reply_teams(interaction, 2)


@app_commands.command()
@app_commands.guild_only()
async def squad(interaction: discord.Interaction) -> None:
    """1 チームあたり 4 人に近くなるよう均等にチーム分けする"""
    await reply_teams(interaction, 4)


@app_commands.command()
@app_commands.guild_only()
@app_commands.describe(size="1 チームあたりの人数")
async def team(
    interaction: discord.Interaction, size: app_commands.Range[int, 1]
) -> None:
    """指定人数に近くなるよう均等にチーム分けする"""
    await reply_teams(interaction, size)


@app_commands.command()
@app_commands.describe(sides="ダイスの面の数 (省略すると 6)")
async def dice(
    interaction: discord.Interaction, sides: app_commands.Range[int, 1] = 6
) -> None:
    """1 から指定の数までのダイスを振る"""
    await interaction.response.send_message(str(random.randint(1, sides)))


class TeamBot(discord.Client):
    def __init__(self, dev_guild_id: int | None) -> None:
        # VC の参加者の取得にはサーバーと VC の参加状況のキャッシュがあれば足りるので、使わないイベントを受け取らないよう、その 2 つに対応する intents だけを有効にする
        intents = discord.Intents.none()
        intents.guilds = True
        intents.voice_states = True
        super().__init__(
            intents=intents, allowed_mentions=discord.AllowedMentions.none()
        )
        self.dev_guild_id = dev_guild_id
        self.tree = app_commands.CommandTree(self)
        for command in (duo, squad, team, dice):
            self.tree.add_command(command)

    async def setup_hook(self) -> None:
        if self.dev_guild_id is None:
            await self.tree.sync()
            return

        # サーバー単位の登録は即時に反映されるので、開発中は指定のサーバーだけに登録して変更をすぐ試せるようにする
        guild = discord.Object(id=self.dev_guild_id)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def on_ready(self) -> None:
        LOGGER.info("Logged in as %s (ID: %s)", self.user, self.user.id)


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        sys.exit("BOT_TOKEN is not set")

    dev_guild_id = os.environ.get("DEV_GUILD_ID")
    client = TeamBot(int(dev_guild_id) if dev_guild_id else None)
    client.run(token, root_logger=True)


if __name__ == "__main__":
    main()
