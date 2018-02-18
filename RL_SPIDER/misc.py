#C:\Users\saurabhj\OneDrive\Documents\Python Scripts\RL\RL_SPIDER
#https://github.com/saurabhjadhav1911/RL.git
import json
import subprocess
import socket
import os
import time
import argparse
from colorama import Fore, Back, Style
import colorama
from functools import reduce
host = None


def read_config():
    filename = os.path.join(os.path.dirname(__file__), 'config.json')
    print(filename)
    with open(filename, "r") as f:
        s = f.read()
        config = json.loads(s)
    return config


def get_ip_mac():
    config = read_config()
    mac = config['GUI_config']['mac_ros']

    mac = mac.replace(':', '-')
    data = subprocess.check_output(['arp', '-a'])
    #line=data
    data = data.split('\n')
    for line in data:
        if mac in line:
            line = line.split()
            host = line[0]
    if host == None:
        host = get_sock_ip()

    print("ip is {}".format(host))
    return host


def get_sock_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    return host


def save_config(config):
    s = json.dumps(config)
    with open("config.json", "w") as f:
        f.write(s)


def consumer(q):
    while True:
        while q.empty() is False:
            print(q.get())
        time.sleep(0.017)


def flatten(d, pref=''):
    return(reduce(
        lambda new_d, kv: \
            isinstance(kv[1], dict) and \
            {**new_d, **flatten(kv[1], pref + kv[0])} or \
            {**new_d,  kv[0]: [kv[1],pref+'|'+kv[0],]},
        d.items(),
        {}
    ))


def arg_parser(config):
    parser = argparse.ArgumentParser()
    flat_config = flatten(config)
    for var_name in flat_config.keys():
        #print(var_name, flat_config[var_name])
        parser.add_argument(
            '--' + str(var_name),
            type=type(flat_config[var_name][0]),
            default=flat_config[var_name][0],
            help=flat_config[var_name][1] + " of type " +
            str(type(flat_config[var_name][0])))
    args = parser.parse_args()
    conf = args.__dict__
    cf = {}

    def rec(l, v, d):
        if len(l) is 1:
            d[l[0]] = v
        else:
            if l[0] in d:
                d[l[0]] = rec(l[1:], v, d[l[0]])
            else:
                d[l[0]] = rec(l[1:], v, {})
        return d

    for v in conf.keys():
        cf = rec(flat_config[v][1].split('|'), conf[v], cf)
    return cf


def get_ip():
    host = misc.get_ip_mac()
    #host =misc.get_sock_ip()
    print("host:{}".format(host))


def sprint(msg):
    port = 5000
    s = socket.socket()
    s.connect((host, port))
    s.send(msg)
    s.close()


def generate_step(recieve_que, send_que, config):
    vl = 0
    while (1):
        send_que.put(vl)
        vl = 180 - vl
        time.sleep(2)


if __name__ == '__main__':
    print(get_ip())
