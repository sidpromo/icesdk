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

 def test_ice_rest_server_upload(self):
        port = config['config_manager']['ice_rest_service']['port']
        multiple_files = [
            ('files', ('test.so', io.BytesIO(b"abcdef"))),
            ('files', ('test.sig', io.BytesIO(b"abcdef")))]

        folder = config['config_manager']['ice_rest_service']['ice_workdir']
        so_file = Path(folder,'test.so')
        sig_file = Path(folder,'test.sig')

        if so_file.is_file():
            so_file.unlink()
        if sig_file.is_file():
            sig_file.unlink()

        response_msg = get_response_text_from_post(f"http://localhost:{port}/upload", False, 10, multiple_files)

        self.assertEqual(response_msg,'{"message":"File(s) successfully uploaded","success":true}\n')
        self.assertTrue(so_file.is_file() and sig_file.is_file())

    def test_ice_rest_server_download(self):
        port = config['config_manager']['ice_rest_service']['port']
        fname = ''

        try:
            response = get_response(f"http://localhost:{port}/download", False , 10)
            if "Content-Disposition" in response.headers.keys():
                fname = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
        except Exception as e:
            print(e)

        self.assertEqual(fname,'plugins.tar.gz')
	
def get_response_text_from_post(url, tls_enabled, retry_count, files):
    retry = retry_count
    while retry > 0:
        try:
            if tls_enabled:
                response = requests.post(url,files=files, verify=CACERT_PATH.as_posix(), cert=(CLIENT_CERT_PATH.as_posix(), CLIENT_KEY_PATH.as_posix()))
            else:
                response = requests.post(url,files=files)
            return response.text
        except Exception as err:
            print(f"Unexpected error while getting correlator config from REST server at {url}, error: {err}, {type(err)}")
            retry = retry - 1
            time.sleep(1)
from argparse import ArgumentParser
def setup_args():
    parser = ArgumentParser(
        description='Arguments for ICE-SDK file uploader RestAPI')
    parser.add_argument('-w', '--workspace',
                        required=True,
                        action='store',
                        help='Destination directory where the uploaded files are going to be stored.')
    my_args = parser.parse_args()

    return my_args

