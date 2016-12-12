# zombie-slaves.py

## Overview

When jenkins is configured to dynamically spin up slave VMs
in an openstack environment, it is possible for it to lose
track of the slaves and not clean them up properly.
When this happens, the zombie slaves must be cleaned up
to prevent them from consuming brains^h^h^h^h^h^h resources.

## Dependencies

  * python-jenkins https://python-jenkins.readthedocs.io/en/latest/
  * novaclient https://github.com/openstack/python-novaclient
  * ConfigParser

## Configuration file

zombie-slaves.conf must be populated with credentials for
the openstack provider so that the script has the authority
to list existing VMs and delete them.

If Jenkins is configured to require authentication, then those
credentials must be supplied as well.

### Configuration options

  * MAX_SLAVE_LIFE_HOURS

Only consider a slave for deletion if the slave was created
less than this number of hours ago.

  * SLAVE_NAME_PATTERN

Not all VMs are dynamic slaves.  To prevent the accidental
removal of long-running pet VMs, test the name of the instance
against this pattern and only consider matches for deletion.

  * JENKINS_KEY_PATTERN

Some cloud plugins provide metadata that identifies an instance
as a dynamic slave for jenkins.  This is another way to prevent
the accidental deletion of long-running pet VMs.  For instance, 
our openstack plugin adds these metadata keys:
  * jenkins-instance
  * jenkins-template-name
If provided, only consider an instance for deletion if contains
matching metadata keys.

## Usage

The script has no command-line parameters, ie:

  `zombie-slaves.py`

