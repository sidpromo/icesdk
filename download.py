#!/usr/bin/env python3
import requests
import re
import time
from pathlib import Path
from argparse import ArgumentParser

CLIENT_KEY_PATH = Path(
    '/etc/certs/eric-oss-correlator-operator-client-certificate/client-private-key.pem')
CLIENT_CERT_PATH = Path(
    '/etc/certs/eric-oss-correlator-operator-client-certificate/client-cert.pem')
CACERT_PATH = Path(
    '/etc/ca_certs/eric-oss-correlator-operator-ca-cert/cacert.pem')

def get_response(url, retry_count):
    retry = retry_count
    while retry > 0:
        try:
            # response = requests.get(url, verify=CACERT_PATH.as_posix(), cert=(CLIENT_CERT_PATH.as_posix(), CLIENT_KEY_PATH.as_posix()))
            response = requests.get(url)
            return response
        except Exception as err:
            print(
                f"Unexpected error while getting correlator config from REST server at {url}, error: {err}, {type(err)}")
            retry = retry - 1
            time.sleep(1)


def download(args):
    port = 5000
    fname = ''
    try:
        response = get_response(f"http://localhost:{port}/download", 10)
        if "Content-Disposition" in response.headers.keys():
            fname = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
            p = Path()/Path(fname)
            if args.workdir is not None:
                p = Path(args.workdir)/Path(fname)
            open(p, 'wb').write(response.content)
            print(f"File: {fname} downloaded to {p.absolute()}")
    except Exception as e:
        print(e)


def setup_args():
    parser = ArgumentParser(
        description='Arguments for ICE SDK file downloader')
    parser.add_argument('-w', '--workdir',
                        required=False,
                        action='store',
                        help='Directory where the plugins will be downloaded to.')
   
    my_args = parser.parse_args()
    if my_args.workdir is not None and not Path(my_args.workdir).is_dir():
        print("The given download directory doesn't exist.")

    return my_args

args = setup_args()
download(args)
