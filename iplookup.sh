#!/bin/sh

servers=( 
127.0.0.1
)

for i in "${servers[@]}"; do
    echo "server: $i" 
    echo `ssh root@$i "hostname"` >> glustnames.txt
    echo "server: $i" >> glustnames.txt
done
