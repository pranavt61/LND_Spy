# Script to move coins through network
#   ulilizing bash commands
#   NOTE:   probably not the nest way to implement this
#           try RPC
import subprocess
import json
import time
import random

# find lnd nodes and ports
ln = [
    'lncli --rpcserver=localhost:10001 --no-macaroons ',
    'lncli --rpcserver=localhost:10003 --no-macaroons '
];

ln_names = [
    'Alice',
    'Charlie'
];

def main():
    # send coins every n seconds
    while True:
        s = -1
        r = -1
        a = 1

        # pick random sender
        s = random.randint(0, len(ln) - 1);

        # pick random receiver
        r = random.randint(0, len(ln) - 1);
        while r == s:
            # pick another val
            r = random.randint(0, len(ln) - 1);

        # pick random amount
        a = random.randint(1, 10)

        send_coins(s, r, a);

        time.sleep(2);

def cmd(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE);
    output, error = process.communicate();

    return output

def send_coins(sender , receiver, amt):
    print(ln_names[sender] + ' paying ' + ln_names[receiver] + ' ' + str(amt) + ' coins' + '...');

    # make invoice
    add_invoice = ln[receiver] + 'addinvoice --amt=' + str(amt);
    invoice_string = cmd(add_invoice);

    invoice = json.loads(invoice_string);

    # pay invoice
    pay_invoice = ln[sender] + 'sendpayment -f --pay_req=' + invoice['pay_req'];

    receipt = cmd(pay_invoice);
    receipt = json.loads(receipt);

    if receipt['payment_error'] == '':
        print("Success")
        print("---------------------------------------")
    else:
        print("FAILED")
        print(receipt)
        print("---------------------------------------")

main();
