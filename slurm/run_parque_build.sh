#!/bin/bash
cd /home/u/tknab/mypythonenv
source venv/bin/activate
bucket="mybucketname"
folder="myfoldername"
cost="1.581"
sudo cat /var/log/slurmctld.log | python3 $HOME/cronjobs/parquet_log_building1mo.py -C $cost --s3-bucket $bucket/$folder
deactivate
