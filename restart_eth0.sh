while true
    do
      ip link set dev eth0 down > /dev/null 2>&1
      ip link set dev eth0 up > /dev/null 2>&1
      echo "restart eth0 interface" $(date) >> /var/log/connection.log
      sleep 10800
    done
