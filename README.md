# teambot

ボイスチャンネル (VC) にいるメンバーを、ランダムにチーム分けする Discord bot です。

PUBG や Apex Legends のような、3〜4 人でチームを組むゲームのコミュニティでの利用を想定しています。

## コマンド

コマンドはすべてスラッシュコマンドです。

### チーム分け

コマンドを実行した人が入っている VC のメンバーを、ランダムにチーム分けします。

- `/duo`
  - 1 チーム 2 人に近くなるよう分けます
- `/squad`
  - 1 チーム 4 人に近くなるよう分けます
- `/team size:3`
  - 1 チームを指定した人数に近くなるよう分けます

各チームの人数の差は 1 人までに収まります。
たとえば 15 人で `/squad` を実行すると、3 人、4 人、4 人、4 人の 4 チームになります。

### ダイス

- `/dice`
  - 1〜6 の数をランダムに返します
- `/dice sides:10`
  - 1〜10 の数をランダムに返します
  - 面の数は自由に指定できます

## Discord 側の設定

- [Developer Portal](https://discord.com/developers/applications) でアプリケーションを作り、bot のトークンを取り出します
- 特権 intent は、どれも有効にしなくて構いません
- Discord のサーバーには `bot` の scope で招待し、次の権限を付けます
  - View Channels
  - Send Messages
- `bot` の scope を付けずに招待すると、bot が Discord のサーバーのメンバーになりません
  - その場合、チーム分けのコマンドは VC のメンバーを読み取れず、「ボイスチャンネルに入ってから実行してください」と返します

## 常駐させる

bot を動かすマシンに [Docker](https://docs.docker.com/) と Docker Compose を入れておきます。

```bash
git clone https://github.com/hidekuro/teambot
cd teambot

# .env を作り、BOT_TOKEN に bot のトークンを書く
cp .env.example .env

# バックグラウンドで起動する
docker compose up -d --build

# ログを見る
docker compose logs -f

# 止める
docker compose down
```

止めない限り、異常終了やマシンの再起動の後にも自動で立ち上がります。

## 開発

開発には [uv](https://docs.astral.sh/uv/getting-started/installation/) を使います。

- 必要な Python は uv が自動で入れます
- Python のバージョンは `.python-version` に書いてあります
- 開発用の bot には、常駐させている bot とは別のアプリケーションを使います
  - 同じアプリケーションで `DEV_GUILD_ID` を使うと、常駐させている bot が登録したコマンドと二重に表示されます

```bash
# 依存パッケージを .venv に入れる
uv sync

# 手元で起動する
uv run --env-file .env teambot.py
```

`.env` の `DEV_GUILD_ID` に Discord のサーバーの ID を書くと、コマンドをその Discord のサーバーだけに登録します。
Discord のサーバー単位の登録はすぐに反映されるので、コマンドの変更をすぐに試せます。

[Ruff](https://docs.astral.sh/ruff/) で検査と整形をします。

```bash
uv run ruff check
uv run ruff format
```

[Pyright](https://microsoft.github.io/pyright/) で型を検査します。

```bash
uv run pyright
```

[pytest](https://docs.pytest.org/) でテストを実行します。

```bash
uv run pytest
```

## ライセンス

MIT License
