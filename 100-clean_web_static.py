#!/usr/bin/python3
""" test file """
import os.path
import os
from fabric.api import *
from fabric.operations import run, put, sudo
import time
env.hosts = ['34.207.120.94', '52.87.19.84']


def do_pack():
    timestr = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(timestr))
        return ("versions/web_static_{}.tgz".format(timestr))
    except Exception as e:
        print("Exception:", str(e))
        return False


def do_deploy(archive_path):
    """Archive distributor"""
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        nconfig = archive_path.split("/")[-1]
        ndir = ("/data/web_static/releases/" + nconfig.split(".")[0])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(ndir))
        run("sudo tar -xzf /tmp/{} -C {}".format(nconfig, ndir))
        run("sudo rm /tmp/{}".format(nconfig))
        run("sudo mv {}/web_static/* {}/".format(ndir, ndir))
        run("sudo rm -rf {}/web_static".format(ndir))
        run('sudo rm -rf /data/web_static/current')
        run("sudo ln -s {} /data/web_static/current".format(ndir))
        return True
    except Exception as e:
        print("Exception:", str(e))
        return False


def deploy():
    """Pack and deploy all file """
    try:
        archive_address = do_pack()
        val = do_deploy(archive_address)
        return val
    except Exception as e:
        print("Exception:", str(e))
        return False


def do_clean(number=0):
    """Cleans all .tgz files"""
    number = 1 if int(number) == 0 else int(number)

    files = sorted(os.listdir("versions"))
    [files.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(j) for j in files)]

    with cd("data/web_static/releases"):
        files = run("ls -tr").split()
        files = [j for j in files if "web_static_" in j]
        [files.pop() for i in range(number)]
        [run("sudo rm -rf ./{}".format(j)) for j in files]
