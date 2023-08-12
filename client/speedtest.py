import re
import os
import subprocess
import logging
from influxdb import InfluxDBClient

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

logging.info('Calling speedtest.net API...')
response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

# Sample response from the Okkla Speedtest CLI
""" 
   Speedtest by Ookla

      Server: GSL Networks - New York, NY (id: 99999)
         ISP: Packethub s.a.
Idle Latency:    21.19 ms   (jitter: 0.33ms, low: 20.38ms, high: 21.30ms)
    Download:   394.73 Mbps (data used: 481.0 MB)
                470.89 ms   (jitter: 88.55ms, low: 23.93ms, high: 2454.44ms)
      Upload:   222.61 Mbps (data used: 394.0 MB)
                 30.81 ms   (jitter: 6.65ms, low: 21.07ms, high: 262.71ms)
 Packet Loss:    32.5%
  Result URL: https://www.speedtest.net/result/c/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
 """

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)
jitter = jitter.group(1)

speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "RaspberryPi"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping),
            "jitter": float(jitter)
        }
    }
]

# https://influxdb-python.readthedocs.io/en/latest/api-documentation.html
# The backend DNS name comes from the `name` field in the backend service `.yaml` file

client = InfluxDBClient(os.getenv('TIME_SERIES_HOST'), 
                        os.getenv('TIME_SERIES_PORT'),
                        os.getenv('TIME_SERIES_USERNAME'), 
                        os.getenv('TIME_SERIES_PASSWORD'), 
                        os.getenv('TIME_SERIES_DATABASE'))

logging.info('Writing speed data to time series database.')
client.write_points(speed_data)
