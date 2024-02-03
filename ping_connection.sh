#!/bin/bash

host="8.8.8.8"

allowed_failures=3

while true; do
    failed_count=0
    for ((i=1; i<=allowed_failures; i++)); do
        ping -c 1 -W 1 $host > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            failed_count=$((failed_count + 1))
        fi
    done

    if [ $failed_count -eq $allowed_failures ]; then
        echo "connection failed!" $(date +"%Y-%m-%d %H:%M:%S") >> /var/log/connection.log
        echo "connection failed!" $(date +"%Y-%m-%d %H:%M:%S")
        ip link set dev eth1 down > /dev/null 2>&1
        ip link set dev eth1 up > /dev/null 2>&1
        sleep 60
    fi

    sleep 1
done

