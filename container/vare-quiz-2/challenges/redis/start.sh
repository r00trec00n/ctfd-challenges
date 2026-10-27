#!/bin/sh
set -eu
redis-server /app/redis.conf &
redis_pid=$!
trap 'kill -TERM "$redis_pid" 2>/dev/null || true; wait "$redis_pid" 2>/dev/null || true; exit 0' TERM INT
ready=0
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    if redis-cli -h 127.0.0.1 -p 6379 PING >/dev/null 2>&1; then ready=1;break;fi
    sleep 1
done
if [ "$ready" != 1 ]; then kill "$redis_pid" 2>/dev/null || true;exit 1;fi
flag="${FLAG:-$(cat /app/flag.txt)}"
redis-cli SET lab:cache:status 'ready' >/dev/null
redis-cli SET lab:internal:assessment "$flag" >/dev/null
redis-cli SET lab:cache:release '2026.10' >/dev/null
# Keep the intended unauthenticated read exposure, but prevent students modifying data.
redis-cli ACL SETUSER default on nopass '~*' -@all +ping +info +scan +get +select +quit +hello '+client|setinfo' >/dev/null
printf 'VARE infrastructure lab is ready\n'
wait "$redis_pid"
