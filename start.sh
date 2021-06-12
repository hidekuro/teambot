#!/bin/bash
set -e
cd $(dirname $0)

PID=teambot.pid

if [[ -e teambot.pid ]]; then
  kill -TERM $(cat $PID) || true
  rm $PID
fi

source .venv/bin/activate

set -a
source .env
set +a

nohup python teambot.py >/dev/null 2>&1 &

echo $! > $PID

echo "start in background [$(cat $PID)]"
