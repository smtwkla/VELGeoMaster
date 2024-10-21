#!/usr/bin/env bash
cd /home/frappe/
bench init --skip-redis-config-generation frappe-bench
cd frappe-bench
bench set-config -g db_host db
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
bench set-config -g redis_socketio redis://redis-queue:6379
git config --global --add safe.directory '*'
bench get-app vel_geo_master /workspace/
bench config set-common-config -c root_password '"admin"'
bench new-site --no-mariadb-socket --admin-password admin vel_geo_master_dev
bench --site vel_geo_master_dev set-config developer_mode 1
bench --site vel_geo_master_dev clear-cache
bench --site vel_geo_master_dev install-app vel_geo_master
bench use vel_geo_master_dev
rm -Rvf apps/vel_geo_master
ln -s /workspace apps/vel_geo_master
