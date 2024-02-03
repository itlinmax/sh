#!/bin/bash
domain="www.google.com"
port=443
timeout=5
number_of_allowed_errors=3

check_conn () {
    nc_status=$(timeout "${timeout}" nc -z "${domain}" "${port}" &> /dev/null ; echo $?)
    echo "$nc_status"
}


while true
do
  errors=0
  for i in $(seq "$number_of_allowed_errors")
  do
    status="$(check_conn)"
    #echo "$status"
    if [ "$status" -ne 0 ]
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
