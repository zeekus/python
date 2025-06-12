#!/bin/bash
#run a read of the data file. 
cd $HOME/mypythonenv
source venv/bin/activate
python3 $HOME/cronjobs/parquet_retrival_gold.py
deactivate
