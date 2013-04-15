#!/usr/bin/env python

import os
import sys
import subprocess

PG_VERSION = os.environ.get('PGVERSION')
PYTHON_2_6 = sys.version_info < (2, 7)

sql = '''
CREATE USER ckanuser WITH PASSWORD 'pass';
CREATE USER readonlyuser WITH PASSWORD 'pass';

CREATE DATABASE ckan_test WITH OWNER ckanuser;
CREATE DATABASE ckan_test_datastore WITH OWNER ckanuser;
'''


def shell(arg):
    subprocess.call(arg)

# Install postgres and solr
# We need this ppa so we can install postgres-8.4
shell(['sudo', 'add-apt-repository', '-yy', 'ppa:pitti/postgresql'])
shell(['sudo', 'apt-get', 'update', '-qq'])
shell(['sudo', 'apt-get', 'install', 'solr-jetty', 'postgresql-%s' % PG_VERSION])

shell(['psql', '-U', 'ckanuser', 'ckan_test', '-c', 'SELECT version();'])
