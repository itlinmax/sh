#!/bin/bash
domain="https://www.google.com"
number_of_allowed_errors=3
timeout=5

check_conn () {
    curl_status=$(timeout "${timeout}" curl -I --insecure -s -o /dev/null -w "%{http_code}" "${domain}")
    echo "$curl_status"
}


while true
do
  errors=0
  for i in $(seq "$number_of_allowed_errors")
  do
    status="$(check_conn)"
    #echo "$status"
    if ! [[ "$status" -ge 200 ]] || ! [[  "$status" -le 299 ]]
    then
      ((errors++))
      if [ "$errors" -eq "$number_of_allowed_errors" ]
      then
        echo "connection failed!" status_code [$status] $(date +"%Y-%m-%d %H:%M:%S")
        ip link set dev eth1 down > /dev/null 2>&1
        ip link set dev eth1 up > /dev/null 2>&1
        sleep 60
      fi
    fi
  done
  sleep 1
done
