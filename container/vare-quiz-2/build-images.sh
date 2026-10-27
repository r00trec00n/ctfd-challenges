#!/bin/sh
set -eu
cd "$(dirname "$0")"
docker compose -f compose.yaml build
printf '\nImages built. Configure CTFd from instructor/FLASH2K_SETUP.md.\n'
