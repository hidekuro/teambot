import logging
import os
import random
import sys

import discord
from discord import app_commands

LOGGER = logging.getLogger(__name__)


def team_alloc(members: list, alloc_size: int) -> list:
    """指定の割り当てサイズに近い人数で均等にチーム分配する

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
    for s in sizes:
        team = []
        for _ in range(s):
            m = next(members_iter)
            team.append(m)
        result.append(team)

    return result


def team_to_string(teams: list[list[discord.Member]]) -> str:
    """チームのリストを表す2次元リストの文字列表現を取得する

    Args:
        teams: チームのリストを表す2次元リスト

    Returns:
        文字列表現
    """
    return "".join(
        f"[Team {i + 1}] {', '.join(m.display_name for m in t)}\n"
        for i, t in enumerate(teams)
    )


async def reply_teams(interaction: discord.Interaction, alloc_size: int) -> None:
    """実行した人の VC にいるメンバーをチーム分けし、返答する

    Args:
        interaction: スラッシュコマンドの interaction
        alloc_size: 1チームあたりの人数
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
    """1チームあたり2人に近くなるよう均等にチーム分けする"""
    await reply_teams(interaction, 2)


@app_commands.command()
@app_commands.guild_only()
async def squad(interaction: discord.Interaction) -> None:
    """1チームあたり4人に近くなるよう均等にチーム分けする"""
    await reply_teams(interaction, 4)


@app_commands.command()
@app_commands.guild_only()
@app_commands.describe(size="1チームあたりの人数")
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
    """1から指定数値までのダイスを振る"""
    await interaction.response.send_message(str(random.randint(1, sides)))


class TeamBot(discord.Client):
    def __init__(self, dev_guild_id: int | None) -> None:
        super().__init__(intents=discord.Intents.default())
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
