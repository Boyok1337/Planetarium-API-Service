#!/bin/sh

host="$1"
shift
port="$1"
shift

timeout="${WAITFORIT_TIMEOUT:-15}"
interval="${WAITFORIT_INTERVAL:-1}"
cmd="$@"

while ! nc -z $host $port; do
  timeout=$((timeout - interval))
  if [ $timeout -le 0 ]; then
    echo "Timeout! $host:$port is not available"
    exit 1
  fi
  sleep $interval
done

exec $cmd
