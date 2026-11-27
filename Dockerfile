# Dependabot が uv のイメージも更新できるよう、COPY --from に直接書かずにステージとして読み込む
FROM ghcr.io/astral-sh/uv:0.13.10 AS uv

FROM python:3.15-slim-trixie AS builder
COPY --from=uv /uv /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-dev --no-install-project

FROM python:3.15-slim-trixie
RUN useradd --system --no-create-home teambot
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY teambot.py ./
ENV PATH="/app/.venv/bin:$PATH"
USER teambot
# PID 1 の Python は SIGTERM を無視するので、discord.py が接続を閉じて終われる SIGINT で止める
STOPSIGNAL SIGINT
CMD ["python", "teambot.py"]
