#!/usr/bin/env bash

if [ -z "$APP" ]; then
  echo "Error: APP variable is not set or empty."
  exit 1
fi

cd /home/frappe/frappe-bench
bench new-app $APP
mv apps/${APP} /workspace
ln -s /workspace apps/${APP}
bench --site ${APP}_dev install-app ${APP}
