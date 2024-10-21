#!/usr/bin/env bash
cd /home/frappe/
bench init --skip-redis-config-generation frappe-bench
cd frappe-bench
bench set-config -g db_host db
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
bench set-config -g redis_socketio redis://redis-queue:6379
git config --global --add safe.directory '*'
