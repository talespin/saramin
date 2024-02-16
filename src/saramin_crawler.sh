#!/bin/bash

cd /mnt/work/saramin/src

while :
do
    python 1.saramin_list.py -y=yes
    python 3.saramin_crawler_master.py
    echo "1시간 쉬었다가 다시 시작합니다."
    sleep 1h
done

