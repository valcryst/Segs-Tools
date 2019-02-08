#!/usr/bin/python

import requests
import socket
import json
import time


def get_SegsData():
    # AdminRPC Endpoint
    host = "10.25.0.136"
    port = 6001
    # InfluxDB Settings
    use_influxdb  = "false"
    influxdb_user = "xxxx"
    influxdb_pass = "xxxx"
    influxdb_db   = "xxxx"
    influxdb_url  = "http://domain.local:8086"

    # Connect to AdminRPC
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # getVersion
    s.sendall(b"{ \"jsonrpc\":\"2.0\", \"method\":\"getVersion\", \"params\": {}, \"id\": 1 }")
    segs_version = json.loads(s.recv(140))
    # getCodename
    s.sendall(b"{ \"jsonrpc\":\"2.0\", \"method\":\"getCodename\", \"params\": {}, \"id\": 1 }")
    segs_codename = json.loads(s.recv(140))
    # getStartTime
    s.sendall(b"{ \"jsonrpc\":\"2.0\", \"method\":\"getStartTime\", \"params\": {}, \"id\": 1 }")
    segs_starttime = json.loads(s.recv(140))

    # Disconnect from AdminRPC
    s.close()

    if use_influxdb == "false":
      # Use with Telegraf exec.input or as debug output
      print("segs,host=" + socket.gethostname() + \
              " version=" + segs_version['result'] + \
              ",codename=" + segs_codename['result'] + \
              ",start_time=" + segs_starttime['result'] + \
              " " + str(time.time()).split('.')[0] + "000000000")
    else:
      # Sent to InfluxDB
      data = 'segs,host=' + socket.gethostname() + \
              ' version="' + segs_version['result'] + \
              '",codename="' + segs_codename['result'] + \
              '",start_time=' + segs_starttime['result'] + \
              ' ' + str(time.time()).split('.')[0] + '000000000'

      influx_write = requests.post(influxdb_url + \
              '/write?db=' + influxdb_db, \
              data=data, \
              auth=(influxdb_user, influxdb_pass))

if __name__ == "__main__":
      get_SegsData()
