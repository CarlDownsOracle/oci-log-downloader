# OCI Log Downloader

Invoke the program like so:

## Specific Time Frame

Pull the entries from a given Log that were written in between specific start and end times: 


    $venv python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_logs2.json \
    start_time_iso_format=2023-07-11T00:26:27 \
    end_time_iso_format=2023-07-11T00:27:27

_ISO format supported: "%Y-%m-%dT%H:%M:%S"_

## Relative Time Frame

Pull the last 5 minutes of entries from a given Log: 

    $venv python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_logs2_relative.json \
    start_time_minutes_ago=5 \
    end_time_minutes_ago=0


## Relative Time Frame, Entire Compartment

Pull the last 2 minutes of entries from all logs within a given Compartment:

    $venv python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    output_file=./oci_logs2_comp.json \
    start_time_minutes_ago=2 \
    end_time_minutes_ago=0
