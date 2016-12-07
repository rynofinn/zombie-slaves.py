#!/usr/bin/python

import ConfigParser
from datetime import datetime,timedelta
from novaclient import client
import jenkins

config = ConfigParser.ConfigParser()
config.read('zombie-slaves.conf')

VERSION = config.get('cloud','VERSION')
USERNAME = config.get('cloud','USERNAME')
PASSWORD = config.get('cloud','PASSWORD')
PROJECT_ID = config.get('cloud','PROJECT_ID')
AUTH_URL = config.get('cloud','AUTH_URL')
MAX_SLAVE_LIFE_HOURS = config.getint('jenkins','MAX_SLAVE_LIFE_HOURS')
JENKINS_URL = config.get('jenkins','JENKINS_URL')
JENKINS_USER = config.get('jenkins','JENKINS_USER')
JENKINS_PASS = config.get('jenkins','JENKINS_PASS')
SLAVE_NAME_PATTERN = config.get('jenkins','SLAVE_NAME_PATTERN')
JENKINS_KEY_PATTERN = config.get('jenkins','JENKINS_KEY_PATTERN')

def isactive( nodename ):
    active = False
    for n in jenkinsnodes:
        if nodename == n['name']:
            active = True
    return active;

# get list of minions according to jenkins
jenkins_server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_PASS)
jenkinsnodes = jenkins_server.get_nodes()
print "== Slaves that jenkins knows about:"
for node in jenkinsnodes:
    #print node
    print "name: ",node['name']
    print "offline: ",node['offline']
print "----------------------"

MAX_TIMESTAMP = datetime.utcnow() - timedelta(hours=MAX_SLAVE_LIFE_HOURS)
NOW = datetime.utcnow()
#print "NOW is ",NOW
print "== Slaves that Vexx knows about:"
nova = client.Client(VERSION, USERNAME, PASSWORD, PROJECT_ID, AUTH_URL)

for server in nova.servers.list(detailed=True):
    if SLAVE_NAME_PATTERN in server.name:
        foundslavemetadata = 0
        print "server name matching slave pattern: ",server.name
        for key in server.metadata.iterkeys():
            # don't have to look at the value, just the key
            if JENKINS_KEY_PATTERN in key:
                foundslavemetadata = 1
        if foundslavemetadata:
            print "server has slave metadata: passed"
            created = datetime.strptime(server.created, '%Y-%m-%dT%H:%M:%SZ')
            #print "server created: ",created
            age = NOW - created
            print "server age: ",age
            if isactive(server.name):
                print "node is still active in jenkins"
            else:
                print "node is no longer active in jenkins"
                # don't read this as "if created less than timestamp"
                # read it as "if created before timestamp"
                if created < MAX_TIMESTAMP:
                    print "Deleting slave that is older than %d hours and unknown to jenkins" % MAX_SLAVE_LIFE_HOURS
                    server.delete()
