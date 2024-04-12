from .common import prettylog
import os
import subprocess
import time
import sys
import redis
import pprint
import json
import CloudFlare

def cloudflare():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get()
    prettylog("INFO", "Zones", zones)
    return True


def getenv(key, default):
    if key in os.environ:
        return os.environ[key]
    else:
        return default

def main():
    prettylog("INFO", )
    return True

def in_venv():
    return sys.prefix != sys.base_prefix

def init_service():
    prettylog("INFO", "Init service")

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
    prettylog("INFO", "Write service file")
    write_string_to_file(servicefilename, servicefile )
    prettylog("INFO", "Reload daemon")
    subprocess.run(["systemctl", "daemon-reload"])
    prettylog("INFO", "Enable service")
    subprocess.run(["systemctl", "enable", "ign8"])

def check_redis():
    prettylog("INFO", "Check redis")
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
    except redis.ConnectionError:
        prettylog("ERROR", "Redis is not running")
        prettylog("INFO", "Starting Redis")
        subprocess.run(["systemctl", "start", "redis"])
    else:
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

    prettylog("INFO", "Create config file")
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
        prettylog("INFO", "Config file does not exist")
        if create_config_file():
            prettylog("INFO", "Config file created")
        else:
            prettylog("ERROR", "Config file could not be created")
            return False


        
    open('/etc/ign8/config.json', 'r').read()
    myconfig = json.loads(open('/etc/ign8/config.json', 'r').read())
    #set the environment for cloudflare
    


    prettylog("INFO", "Read config", myconfig)
    return myconfig








def start_service():
    prettylog("INFO", "start service")
    subprocess.run(["systemctl", "start", "ign8"])


def stop_service():
    prettylog("INFO", "stop service")
    subprocess.run(["systemctl", "stop", "ign8"])

def serve():
    prettylog("INFO", "Serve")
    init_service()
    cloudflare()
    prettylog("INFO", "Start loop")
    while True:
        prettylog("INFO", "Start loop")
        cloudflare()
        prettylog("INFO", "Sleeping")
        time.sleep(3)

        prettylog("info" , "Start loop")
        check_redis()
        myconfig = read_config()
        if not myconfig:
            prettylog("ERROR", "Config file not found")
            break
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




