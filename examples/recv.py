#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show receiving events from an Event Hub partition and processing
the event in on_event_data callback.

"""

import sys
import logging
from eventhubs import EventHubClient, Receiver, Offset

import examples
logger = examples.get_logger(logging.INFO)

class MyReceiver(Receiver):
    def __init__(self, partition):
        super(MyReceiver, self).__init__()
        self.partition = partition
        self.total = 0
        self.last_sn = -1
        self.last_offset = "-1"

    def on_event_data(self, event_data):
        self.last_offset = event_data.offset
        self.last_sn = event_data.sequence_number
        self.total += 1
        logger.info("Partition %s, Received %s, sn=%d offset=%s",
                     self.partition,
                     self.total,
                     self.last_sn,
                     self.last_offset)

try:
    ADDRESS = ("amqps://"
               "<SAS-policy>"
               ":"
               "<SAS-key>"
               "@"
               "<mynamespace>.servicebus.windows.net"
               "/"
               "myeventhub")
    CONSUMER_GROUP = "$default"
    OFFSET = Offset("-1")

    EventHubClient(ADDRESS if len(sys.argv) == 1 else sys.argv[1]) \
        .subscribe(MyReceiver("0"), CONSUMER_GROUP, "0", OFFSET) \
        .run()

except KeyboardInterrupt:
    pass
