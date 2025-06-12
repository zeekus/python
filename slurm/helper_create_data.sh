#!/bin/bash
cd $HOME/mypythonenv
source venv/bin/activate
cost="1.591"
bucket="mybucket"
folder="myfolder"
sudo cat /var/log/slurmctld.log | python3 $HOME/cronjobs/parquet_log_building1mo.py -C $cost --s3-bucket $bucket/$folder
deactivate
