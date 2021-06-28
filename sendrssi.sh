
#!/bin/bash
mac=D0:5A:FD:5A:54:E2
server=192.168.1.10
port=8080

label=P1

period=0.5

getRSSI () {
  hcitool rssi $mac 2> /dev/null|grep -P '\-?[0-9]+' -o
}

toloop () {
  rssi=$(getRSSI)
  if  [ -z "$rssi" ] ; then
    # recreate baseband conection
    sudo hcitool cc $mac  2> /dev/null
  else
    echo $label:$rssi
    echo $label:$rssi|nc $server $port -N
  fi

  sleep $period
}

while true; do
  toloop 
done
