#!/usr/bin/python3
"""
Fabric script based on 1-pack_web_static.py that distributes
an archive to my web servers using function do_deploy
"""

from fabric import api
from fabric.contrib import files
import os

api.env.hosts = ['54.146.68.43', '18.233.65.183']
api.env.user = 'ubuntu'
api.env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Function to transfer `archive_path` to web servers.
    Args:
        archive_path (str): path of the .tgz file to transfer
    Returns: True on success, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False
    with api.cd('/tmp'):
        basename = os.path.basename(archive_path)
        root, ext = os.path.splitext(basename)
        outpath = '/data/web_static/releases/{}'.format(root)
        try:
            putpath = api.put(archive_path)
            if files.exists(outpath):
                api.run('rm -rdf {}'.format(outpath))
            api.run('mkdir -p {}'.format(outpath))
            api.run('tar -xzf {} -C {}'.format(putpath[0], outpath))
            api.run('rm -f {}'.format(putpath[0]))
            api.run('mv -u {}/web_static/* {}'.format(outpath, outpath))
            api.run('rm -rf {}/web_static'.format(outpath))
            api.run('rm -rf /data/web_static/current')
            api.run('ln -sf {} /data/web_static/current'.format(outpath))
            print('New version deployed!')
        except:
            return False
        else:
            return True