# Script to manage spynodes and data
#   NOTE: Using bash commands, probably best to use gRPC
from __future__ import print_function
import re
import subprocess
import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import os
import time

# define spynodes
start_spy = [
    'lnd --datadir=~/gocode/dev/b/data/ --logdir=~/gocode/dev/b/log/ --debuglevel=debug --rpclisten=localhost:10002 --listen=localhost:10012 --restlisten=localhost:8002 --no-macaroons'    # Bob
];

unlock_spy = [
    'lncli --rpcserver=localhost:10002 --no-macaroons unlock'   # Bob
];

payments_routed = [];

def main():
    # Due to updated ECDSA generated tls.cert we need to let gprc know that
    # we need to use that cipher suite otherwise there will be a handhsake
    # error when we communicate with the lnd rpc server.
    os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

    start_spy_output = cmd(start_spy[0]);

    # open gRPC connection
    cert = open(os.path.expanduser('~/.lnd/tls.cert'), 'rb').read()
    creds = grpc.ssl_channel_credentials(cert)
    channel = grpc.secure_channel('localhost:10002', creds)
    stub = lnrpc.WalletUnlockerStub(channel)

    # unlock wallet
    # request = ln.UnlockWalletRequest(wallet_password="bbbbbbbb".encode())
    # response = stub.UnlockWallet(request)

    for line in start_spy_output:
        match_r = re.search("((.*)Received UpdateAddHTLC(.*))", line) 
        match_s = re.search("((.*)Sending UpdateAddHTLC(.*))", line)
        if match_r:
            from_addr = line.split(' from ')[1].split('@')[0];
            timestamp = line.split(' [DBG] ')[0];
            from_amt = line.split(', ')[2].split('=')[1];

            print(from_addr + ' - ' + from_amt + ' - ' + timestamp)
        elif match_s:
            print("asdsad")

    return;

def cmd(command):
    print(command)
    popen = subprocess.Popen(command.split(), stdout=subprocess.PIPE, universal_newlines=True);
    for lines in iter(popen.stdout.readline, ""):
        yield lines;
    popen.stdout.close();
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

main();
