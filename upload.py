#!/usr/bin/env python3
import requests
from pathlib import Path
import time

CLIENT_KEY_PATH = Path('/etc/certs/eric-oss-correlator-operator-client-certificate/client-private-key.pem')
CLIENT_CERT_PATH = Path('/etc/certs/eric-oss-correlator-operator-client-certificate/client-cert.pem')
CACERT_PATH = Path('/etc/ca_certs/eric-oss-correlator-operator-ca-cert/cacert.pem')


def get_response(url, retry_count):
	retry = retry_count
	while retry > 0:
		try:
			response = requests.get(url, verify=CACERT_PATH.as_posix(), cert=(CLIENT_CERT_PATH.as_posix(), CLIENT_KEY_PATH.as_posix()))
			return response
		except Exception as err:
			print(f"Unexpected error while getting correlator config from REST server at {url}, error: {err}, {type(err)}")
			retry = retry - 1
			time.sleep(1)


def help():
	print("call api")
	port = 50005
	response_msg = ''
	try:
		response_msg = get_response("https://eric-oss-correlator-operator-service:50005/", 3).text
		print(response_msg)
	except Exception as e:
		print(e)

help() 
