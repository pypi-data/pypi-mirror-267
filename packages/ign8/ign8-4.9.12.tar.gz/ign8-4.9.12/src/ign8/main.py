from .common import prettylog
import os
import subprocess
import time
import sys
import redis
import pprint
import json
import CloudFlare


def read_dns_txt_record(domain):
    command = f"dig {domain} TXT"
    prettylog("INFO", f"Reading DNS TXT record for {domain}")
    result = subprocess.run(command, capture_output=True, shell=True)
    if result.returncode == 0:
        output = result.stdout.decode()
        start_index = output.find('"')
        end_index = output.rfind('"')
        txt_record = output[start_index:end_index + 1]
        txt_record_cleaned = txt_record.strip('"').replace('\\010', '').replace('\\', '')
        pprint.pprint(txt_record_cleaned)

        txt_dict = json.loads(txt_record_cleaned)
        return txt_dict
    else:
        prettylog("ERROR", f"Error reading DNS TXT record for {domain}")
        return False
    

def cloudflare():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get()
    return True


def getenv(key, default):
    if key in os.environ:
        return os.environ[key]
    else:
        return default

def main():
    return True

def in_venv():
    return sys.prefix != sys.base_prefix

def init_service():
    servicefile = "\
[Unit]\n\
Description=Ign8 Service\n\
After=network.target\n\
\n\
[Service]\n\
Type=simple\n\
User=root\n\
ExecStart=/usr/local/bin/ign8 serve\n\
Restart=always\n\
\n\
[Install]\n\
WantedBy=multi-user.target\n\
"
    servicefilename = "/etc/systemd/system/ign8.service"
    write_string_to_file(servicefilename, servicefile )
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ign8"])

def check_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
    except redis.ConnectionError:
        subprocess.run(["systemctl", "start", "redis"])
    prettylog("INFO", "Redis is running")

    
def host_is_up(peer):
    response = os.system("ping -c 1 " + peer)
    if response == 0:
        return True
    else:
        return False




def write_string_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    
    # Create and overwrite the service file"
def create_config_file():
    # create the directory
    if not os.path.exists('/etc/ign8'):
        os.makedirs('/etc/ign8')
    configfile = "\
{\n\
    \"ign8\": {\n\
        \"organisation\": \"ignite\"\n\
    \n\
}\n\
"
    configfilename = "/etc/ign8/config.json"
    write_string_to_file(configfilename, configfile)
    return True

def read_config():
    #check if the file exists
    if not os.path.exists('/etc/ign8/config.json'):
        if not create_config_file():
            return False
    open('/etc/ign8/config.json', 'r').read()
    myconfig = json.loads(open('/etc/ign8/config.json', 'r').read())
    return myconfig

def start_service():
    prettylog("INFO", "start service")
    subprocess.run(["systemctl", "start", "ign8"])


def stop_service():
    subprocess.run(["systemctl", "stop", "ign8"])

def cluster(myconfig):
    try: 
        myorg = myconfig['organisation']
    except:
        myorg = "ajax"
        prettylog("INFO", "No organisation found")
    try: 
        mycluster = myconfig['cluster']
    except:
        mycluster = "default"
        prettylog("INFO", "No cluster found")
    try:
        myservices= myconfig['core_services']
    except:
        prettylog("INFO", "No core services found")

    for clusterserver in mycluster:
        prettylog("INFO", "Cluster server", clusterserver)
        if host_is_up(clusterserver):
            prettylog("INFO", "Host is up     : %s" % clusterserver)
        else:
            prettylog("ERROR", "Host is down  : %s" % clusterserver)
    for service in myservices:
        prettylog("INFO", "Service", service)
        prettylog("INFO", "Sleeping")
    prettylog("INFO", "Config file found")
    prettylog("INFO", "Sleeping")
    time.sleep(3)


def serve():
    init_service()
    while True:
        check_redis()
        myconfig = read_dns_txt_record("core.ign8.it")
        prettylog("INFO", "Reading DNS TXT record for ign8.it")
        cluster(myconfig)


def therest():
        myconfig = read_config()
        try: 
            myorg = myconfig['organisation']
        except:
            myorg = "ajax"
            prettylog("INFO", "No organisation found")
        try: 
            mycluster = myconfig['cluster']
        except:
            mycluster = "default"
            prettylog("INFO", "No cluster found")
        try:
            myservices= myconfig['core_services']
        except:
            prettylog("INFO", "No core services found")

        for clusterserver in mycluster:
            prettylog("INFO", "Cluster server", clusterserver)
            if host_is_up(clusterserver):
                prettylog("INFO", "Host is up     : %s" % clusterserver)
            else:
                prettylog("ERROR", "Host is down  : %s" % clusterserver)
        for service in myservices:
            prettylog("INFO", "Service", service)
            prettylog("INFO", "Sleeping")
        prettylog("INFO", "Config file found")
        prettylog("INFO", "Sleeping")
        time.sleep(3)




