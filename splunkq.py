""""
Test framework for Splunk queries against final data format
"""

import os
import logging
import splunklib.client as SplunkClient
import splunklib.results as SplunkResults
import pprint


class SplunkEventStore():

    def __init__(self, *args, **kwargs):

        # Create a Service instance and log in
        self.service = SplunkClient.connect(
            host=kwargs.get('host'),
            port=kwargs.get('port'),
            username=kwargs.get('username'),
            password=kwargs.get('password')
        )

        # Verify login
        if not self.service.apps:
            raise IOError

    def do_query(self, q, **q_args):

        response = self.service.jobs.oneshot(q, **q_args)
        # Get the results and convert to array of dictionaries using the ResultsReader
        reader = SplunkResults.ResultsReader(response)
        r = []
        for item in reader:
            r.append(dict(item))
        return r


if __name__=="__main__":

    logging.basicConfig(level=logging.DEBUG)

    s = SplunkEventStore(host="localhost",
                         port="8089",
                         username="admin",
                         password="splunk")

    q = "search index=dose StudyDescription=\"*BRAIN*\""
    q_args = {
        "earliest_time": "2017-01-01T12:00:00.000-05:00",
        "latest_time": "2017-01-31T12:00:00.000-05:00"
    }

    r = s.do_query(q, **q_args)

    logging.debug(pprint.pformat(r))





