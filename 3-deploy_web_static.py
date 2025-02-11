#!/usr/bin/python3
""" test file """
import os.path
import time
from fabric.operations import run, put, sudo
from fabric.api import *
env.hosts = ['34.207.120.94', '52.87.19.84']


def do_pack():
    """store path of the created archive"""
    timtr = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".format(timtr))
        return "versions/web_static_{}.tgz".format(timtr)
    except Exception as e:
        print("Exception:", str(e))
        return None


def do_deploy(archive_path):
    """distribute an archive using the new path and archive"""
    if not os.path.isfile(archive_path):
        return False

    try:
        nconfig = archive_path.split("/")[-1]
        ndir = "/data/web_static/releases/" + nconfig.split(".")[0]
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(ndir))
        run("sudo tar -xzf /tmp/{} -C {}".format(nconfig, ndir))
        run("sudo rm /tmp/{}".format(nconfig))
        run("sudo mv {}/web_static/* {}/".format(ndir, ndir))
        run("sudo rm -rf {}/web_static".format(ndir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(ndir))
        return True
    except Exception as e:
        print("Exception:", str(e))
        return False


def deploy():
    """create and distribute an archive to your web servers"""
    try:
        archive_address = do_pack()
        val = do_deploy(archive_address)
        return val
    except Exception as e:
        print("Exception:", str(e))
        return False
