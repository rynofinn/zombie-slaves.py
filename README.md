# zombie-slaves.py

## Overview

When jenkins is configured to dynamically spin up slave VMs
in an openstack environment, it is possible for it to lose
track of the slaves and not clean them up properly.
When this happens, the zombie slaves must be cleaned up
to prevent them from consuming brains^h^h^h^h^h^h resources.

## Dependencies

Requires the python-jenkins package.

## Configuration file

zombie-slaves.conf must be populated with credentials for
the openstack provider so that the script has the authority
to list existing VMs and delete them.

If Jenkins is configured to require authentication, then those
credentials must be supplied as well.

## Usage

The script has no command-line parameters, ie:

  zombie-slaves.py

