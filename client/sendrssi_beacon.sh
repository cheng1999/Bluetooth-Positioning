#!/bin/bash

<<COMMENT
  This client is use for beacon, which check rssi of multiple gateways and send to server.
COMMENT


server=192.168.1.10
port=8080

gateways=(P1 P2 P3)
mac_addrs=(B8:27:EB:EE:E0:9F B8:27:EB:09:79:95 B8:27:EB:06:D6:00)

period=0.5

sendRSSI () {
  label=$1
  macaddr=$2
  rssi=$(hcitool rssi $macaddr 2> /dev/null|grep -P '\-?[0-9]+' -o)
  if  [ -z "$rssi" ] ; then
    # recreate baseband conection
    sudo hcitool cc $macaddr  2> /dev/null
  else
    echo $label:$rssi
    #echo $label:$rssi|nc $server $port -N
  fi

}

while true; do

  for i in ${!gateways[@]}; do
    sendRSSI ${gateways[$i]} ${mac_addrs[$i]}
  done
  sleep $period
done
