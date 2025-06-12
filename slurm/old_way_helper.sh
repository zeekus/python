
list_of_files=$(find /var/log/slurmctld.log*)
for myfile in $list_of_files; do
    echo "processing $myfile"
    sudo cat $myfile | python calculate_aws_hpc_compute_cost.py
done
