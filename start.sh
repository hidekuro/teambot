#!/bin/bash
set -e
cd $(dirname $0)

PID=teambot.pid

if [[ -e teambot.pid ]]; then
  kill -TERM $(cat $PID) || true
  rm $PID
fi

. ENV/bin/activate
. .env

export BOT_TOKEN

nohup python teambot.py >/dev/null 2>&1 &

echo $! > $PID

echo "start in background [$(cat $PID)]"
