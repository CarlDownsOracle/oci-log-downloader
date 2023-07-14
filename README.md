# OCI Log Downloader

This sample program lets you download logs from OCI Logging Service and Audit Service to a local file.

## Authentication

The sample expects to find `~/.oci/config` for authentication.  This is the same configuration file that the OCI CLI also uses.
If you don't want to install the CLI and have OCI Console access, you can create this file manually.

![OCI Console](./images/oci.users.configuration.file.png)

## Run in OCI Cloud Shell

The [OCI Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellquickstart_python.htm) comes
pre-populated with the `~/.oci/config` for authentication. Log files can be subsequently 
[downloaded from Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellgettingstarted.htm#:~:text=To%20download%20a%20file%20from,Shell%20window%20and%20select%20Download.) 
to your local machine.


## Install

Clone the repository, set up your Python virtual environment and install the requirements from with the root directory:

    $ git clone (repo URL)
    $ cd oci-log-downloader
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ (venv) pip install -r requirements.txt

## Usage

Here are some examples of how to invoke the program.

### Specific Time Frame

Download the entries from a given Log that were written in between specific start and end times.
To target a specific Log, you need to pass in the compartment, log and log group OCIDs.


    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_iso_format=2023-07-11T00:26:27 \
    end_time_iso_format=2023-07-11T00:27:27

_ISO format supported: "%Y-%m-%dT%H:%M:%S"_

### Relative Time Frame

Download the last 5 minutes of entries from a given log.

    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_minutes_ago=5 \
    end_time_minutes_ago=0

Download the 1 hours worth of logs from 6 hours ago.

    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_hours_ago=6 \
    end_time_hours_ago=5

Download the last day of entries from a given log.

    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_days_ago=1 \
    end_time_days_ago=0

Download the last week of entries from a given log.

    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_weeks_ago=1 \
    end_time_weeks_ago=0


### All Logs in Log Group

Download the last 5 minutes of entries from a given log group.  Note the
absence of a log OCID.

    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_minutes_ago=5 \
    end_time_minutes_ago=0


### All Logs in Compartment

Downloads the last 60 minutes of entries from *all logs within a given Compartment* including _Audit logs.
Note the absence of log and log group OCIDs.

    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    output_file=./oci_log.json \
    start_time_minutes_ago=60 \
    end_time_minutes_ago=0


### Filtering

Download the log content stanza contains a given string.  The program passes this as a wildcard so
it will return partial matches.


    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_iso_format=2023-07-11T00:26:27 \
    end_time_iso_format=2023-07-11T00:27:27 \
    where_log_content_contains="REJECT"


    $ (venv) python3 main.py \
    compartment_ocid=ocid1.compartment.oc1... \
    log_ocid=ocid1.log.oc1... \
    log_group_ocid=ocid1.loggroup.oc1... \
    output_file=./oci_log.json \
    start_time_iso_format=2023-07-11T00:26:27 \
    end_time_iso_format=2023-07-11T00:27:27 \
    where_log_content_contains="10.0.0.218"