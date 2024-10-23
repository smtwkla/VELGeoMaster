#!/usr/bin/env bash

if [ -z "$APP" ]; then
  echo "Error: APP variable is not set or empty."
  exit 1
fi

cd /home/frappe/
bench init --skip-redis-config-generation frappe-bench
cd frappe-bench
bench set-config -g db_host db
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
bench set-config -g redis_socketio redis://redis-queue:6379
git config --global --add safe.directory '*'
bench config set-common-config -c root_password '"admin"'
bench new-site --no-mariadb-socket --admin-password admin ${APP}_dev
bench --site ${APP}_dev set-config developer_mode 1
bench --site ${APP}_dev clear-cache
bench use ${APP}_dev
