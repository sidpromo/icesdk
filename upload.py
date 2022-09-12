#!/usr/bin/env python3
import requests
import time
from pathlib import Path
from argparse import ArgumentParser

CLIENT_KEY_PATH = Path(
    '/etc/certs/eric-oss-correlator-operator-client-certificate/client-private-key.pem')
CLIENT_CERT_PATH = Path(
    '/etc/certs/eric-oss-correlator-operator-client-certificate/client-cert.pem')
CACERT_PATH = Path(
    '/etc/ca_certs/eric-oss-correlator-operator-ca-cert/cacert.pem')

def get_response_text_from_post(url, retry_count, files):
    retry = retry_count
    while retry > 0:
        try:
            # response = requests.post(url, files=files, verify=CACERT_PATH.as_posix(), cert=(CLIENT_CERT_PATH.as_posix(), CLIENT_KEY_PATH.as_posix()))
            response = requests.post(url, files=files)
            return response.text
        except Exception as err:
            print(
                f"Unexpected error while getting correlator config from REST server at {url}, error: {err}, {type(err)}")
            retry = retry - 1
            time.sleep(1)


def upload(args):
    port = 5000
    so_file = Path(args.so_file)
    sig_file = Path(args.sig_file)

    if not so_file.is_file():
        print('Upload failed, invalid path to the .so file')
        return
    if not sig_file.is_file():
        print('Upload failed, invalid path to the .sig file')
        return

    multiple_files = [
        ('files', (so_file.name, open(so_file, 'rb'))),
        ('files', (sig_file.name, open(sig_file, 'rb')))]

    response_msg = get_response_text_from_post(f"http://localhost:{port}/upload", 3, multiple_files)
    print(response_msg)


def setup_args():
    parser = ArgumentParser(
        description='Arguments for ICE SDK file uploader')
    parser.add_argument('-so', '--so-file',
                        required=True,
                        action='store',
                        help='Path to the so file.')
    parser.add_argument('-sig', '--sig-file',
                        required=True,
                        action='store',
                        help='Path to the sig file.')
    my_args = parser.parse_args()

    return my_args


args = setup_args()
upload(args)
