# teambot

A Discord bot for party players.

teambot will help organize your team.

Especially useful for PUBG players.

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

- Python 3+
- `pip`

## Roles Requirements

- Read Messages
- Send Messages

## Getting started

```bash
# clone repos
git clone https://github.com/hidekuro/teambot
cd teambot

# recommended venv
python3 -m venv .venv
source .venv/bin/activate

# install pip modules
pip install -r requirements.txt

# put your APP BOT USER's Token into .env file
# https://discordapp.com/developers/applications/me
echo BOT_TOKEN=abcde12345yourtoken > .env

# start bot in background
bash ./start.sh
```

## LICENSE

The MIT License.
