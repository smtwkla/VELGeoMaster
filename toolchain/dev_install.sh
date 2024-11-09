#!/usr/bin/env bash

APP=$(head -n 1 /workspace/toolchain/secrets.py | cut -d '=' -f2 | sed 's/^[[:space:]"'\'']*//; s/"$//')
export APP

if [ -z "$APP" ]; then
  echo "Error: APP variable is not set or empty."
  exit 1
fi

cd /workspace/toolchain/

echo "init_bench | new_app | get_app"
read -p "cmd >>> " user_command

if [ "$user_command" = "init_bench" ]; then
    ./dev_init_bench.sh
elif [ "$user_command" = "new_app" ]; then
    ./dev_new_app.sh
elif [ "$user_command" = "get_app" ]; then
    ./dev_get_app.sh
else
    echo "Unknown command"
fi
