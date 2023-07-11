
from datetime import timedelta, datetime, timezone
import json
import oci
import os
from oci.config import from_file
import sys

configuration = from_file(profile_name=os.environ.get('OCI_CLI_PROFILE', 'DEFAULT'))
client = oci.loggingsearch.LogSearchClient(configuration)

"""
# see https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/using_the_api_searchlogs.htm
"""


def get_search_results(query, start_time, end_time):
    """
    Call OCI Logging Service via the SDK
    :param query:
    :param start_time:
    :param end_time:
    :return:
    """

    if start_time > end_time:
        raise RuntimeError('start_time > end_time')

    print(f'query / {query}')
    print(f'start_time / {start_time}')
    print(f'end_time / {end_time}')

    page = None
    log_line_array = []

    details = oci.loggingsearch.models.SearchLogsDetails(time_start=start_time,
                                                         time_end=end_time,
                                                         search_query=query,
                                                         is_return_field_info=False)

    while True:

        response = client.search_logs(search_logs_details=details, limit=10, page=page)
        results = response.data.results

        if results is None:
            break

        for log_entry in results:
            log_line_array.append(log_entry.data)

        print(f'logs downloaded thus far ... {len(log_line_array)}')

        if response.has_next_page:
            page = response.next_page
        else:
            break

    print(f'total logs retrieved = {len(log_line_array)}')
    return log_line_array


def build_query(compartment_ocid, log_group_ocid, log_ocid, where_clause):
    """
    Assemble the log search query.
    :param compartment_ocid: REQUIRED
    :param log_group_ocid: OPTIONAL
    :param log_ocid: OPTIONAL
    :param where_clause: OPTIONAL
    :return: String
    """

    search_scope = 'search "{}"'.format(compartment_ocid)
    log_group_ocid = log_group_ocid.strip() if log_group_ocid else None
    log_ocid = log_ocid.strip() if log_ocid else None

    if log_group_ocid:
        search_scope = 'search "{}/{}"'.format(compartment_ocid, log_group_ocid)

        if log_ocid:
            search_scope = 'search "{}/{}/{}"'.format(compartment_ocid, log_group_ocid, log_ocid)

    if where_clause:
        search_query = '{}|{}'.format(search_scope, where_clause)
    else:
        search_query = search_scope

    return search_query


def get_now_utc():
    return datetime.now(timezone.utc)


def download(query, start_time, end_time, output_file):
    """
    Download the logs and persist to file.
    :param query:
    :param start_time:
    :param end_time:
    :return:
    """

    results_list = get_search_results(query, start_time, end_time)

    if len(results_list):
        print(f'writing logs to file {output_file}')
        with open(output_file, "w") as f:
            json.dump(results_list, f, indent=2)


def main():
    """
    Build the search logs SDK query and time frame, then download and persist the logs as JSON.
    """

    args = sys.argv[1:]
    print(args)

    # compartment OCID is required
    # Log Group, Log and where clause are all optional

    compartment_ocid = 'ocid1.compartment.oc1..'
    log_group_ocid = 'ocid1.loggroup.oc1...'
    log_ocid = 'ocid1.log.oc1...'
    where_clause = None

    query = build_query(compartment_ocid, log_group_ocid, log_ocid, where_clause)

    # a 14-day window is supported

    start_time_iso_format = '2023-07-11 00:26:27.140921+00:00'
    end_time_iso_format = '2023-07-11 00:27:27.140921+00:00'

    # you can use a relative time frame

    use_relative_times = True
    start_minutes_back = 10
    end_minutes_back = 0

    if use_relative_times:
        print(f'using relative time frame from {start_minutes_back} to {end_minutes_back} minutes ago ...')
        start_time = get_now_utc() - timedelta(minutes=start_minutes_back)
        end_time = get_now_utc() - timedelta(minutes=end_minutes_back)

    else:
        start_time = datetime.fromisoformat(start_time_iso_format)
        end_time = datetime.fromisoformat(end_time_iso_format)

    output_file = "./oci_logs.json"
    download(query, start_time, end_time, output_file)


if __name__ == '__main__':
    main()
