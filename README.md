# teambot

A Discord bot for party players.

teambot will help organize your team.

Especially useful for community of games played in teams of 3~4 people. (i.e. PUBG, APEX, Fortnite, etc.)

## Commands Overview

prefix: `*`

### Generate random team

- `*duo` ... Make a random pairs within commander's VC room members.
- `*sq`, `*squad` ... Like above, making 4 peoples team.
- `*team 3` ... Like above, making team with specified size.

For example, There are 15 peoples, and you say `*sq`.
You will get result: 3, 4, 4, and 4 peoples teams.

### Simple dice roll

- `*dice` ... Rolls from 1-6.
- `*dice 10` ... Rolls from 1-10. (or any number would you supplied)

## System Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
  - uv installs the required Python version (see `.python-version`) automatically.

## Roles Requirements

- Read Messages
- Send Messages

## Getting started

```bash
# clone repos
git clone https://github.com/hidekuro/teambot
cd teambot

# install dependencies into .venv
uv sync

# put your bot's token into .env file
# https://discord.com/developers/applications
echo BOT_TOKEN=abcde12345yourtoken > .env

# start bot in foreground
uv run --env-file .env teambot.py

# or start bot in background
# this script creates teambot.pid on current directory.
bash ./start.sh
```

To exit, do the following.

```bash
kill -TERM $(cat teambot.pid)
```

## Development

Lint and format with [Ruff](https://docs.astral.sh/ruff/).

```bash
uv run ruff check
uv run ruff format
```

## LICENSE

The MIT License.
