from __future__ import absolute_import, unicode_literals
from .celery import app
import halocelery.apputils as apputils

import tempfile
import cloudpassage
import os
import time
from datetime import datetime


@app.task
def list_all_groups_formatted():
    halo = apputils.Halo()
    return halo.list_all_groups_formatted()


@app.task
def list_all_servers_formatted():
    halo = apputils.Halo()
    return halo.list_all_servers_formatted()


@app.task
def report_group_formatted(target):
    halo = apputils.Halo()
    return halo.generate_group_report_formatted(target)


@app.task
def report_server_formatted(target):
    """Accepts a hostname or server_id"""
    halo = apputils.Halo()
    return halo.generate_server_report_formatted(target)


@app.task
def servers_in_group_formatted(target):
    """Accepts groupname or ID"""
    # !!! TODO: Need to print the group name at the top of the output!
    halo = apputils.Halo()
    return halo.list_servers_in_group_formatted(target)


@app.task
def scans_to_s3(target_date, s3_bucket_name):
    output_dir = tempfile.mkdtemp()
    halo = apputils.Halo()
    try:
        halo.scans_to_s3(target_date, s3_bucket_name, output_dir)
    except Exception as e:
        "Exception encountered: %s" % e
        "Cleaning up temp dir %s" % output_dir
        raise self.retry(countdown=120, exc=e, max_retries=5)
