#!/usr/bin/env bash

if [ -z "$APP" ]; then
  echo "Error: APP variable is not set or empty."
  exit 1
fi

cd /home/frappe/frappe-bench
bench get-app $APP /workspace/
bench --site ${APP}_dev install-app ${APP}
rm -Rvf apps/${APP}
ln -s /workspace apps/${APP}