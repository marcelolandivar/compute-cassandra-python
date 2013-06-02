#!/usr/bin/env    python
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to set up firewall rules via gcutil."""

import subprocess
import sys
import os

def usage():
    print "Usage: firewall.py [open|close]"
    sys.exit(1)

if len(sys.argv) != 2: usage()

# Assumes user is using the 'default' network
null = open(os.devnull, "w")

if sys.argv[1].lower() == "open":
    ret = subprocess.check_output(["gcutil", "--format", "csv",
            "listfirewalls", "--filter", "name eq cassandra"],
            stderr=null).split('\n')[0:-1]
    if len(ret) == 2:
        raise BaseException("Error: Rule 'cassandra' already exists")

    ret = subprocess.call(["gcutil", "addfirewall",
            "--allowed", "tcp:9160,tcp:9042", "--network", "default",
            "--description", "Allow all incoming to Cassandra Thrift/CQL",
            "cassandra"], stdout=null, stderr=null)
elif sys.argv[1].lower() == "close":
    ret = subprocess.call(["gcutil", "deletefirewall", "--force",
            "cassandra"], stdout=null, stderr=null)
else:
    usage()

if ret != 0:
    print "Error setting firewall rule, please try again"
    sys.exit(ret)
