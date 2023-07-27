#!/usr/local/bin/python3.9

import redis
import sys

working_state = sys.argv[1]
box_IP = sys.argv[2]

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Get the value of the "12" key
input_status = r.get(box_IP + "-12")

# Close the Redis connection
r.close()

# Check the value and print the result

if working_state == "L":
    if input_status == b"0":
        print("ON")
        sys.exit(0)
    elif input_status == b"1":
        print("OFF")
        sys.exit(2)
    else:
        print("Unknown input status")
        sys.exit(3)

if working_state == "H":
    if input_status == b"0":
        print("OFF")
        sys.exit(0)
    elif input_status == b"1":
        print("ON")
        sys.exit(2)
    else:
        print("Unknown input status")
        sys.exit(3)
