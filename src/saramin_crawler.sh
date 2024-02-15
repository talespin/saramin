#!/bin/bash

cd /mnt/work/saramin/src

while :
do
	python 1.saramin_list.py -y=yes;python 3.saramin_crawler_master.py
        sleep 1h
done

