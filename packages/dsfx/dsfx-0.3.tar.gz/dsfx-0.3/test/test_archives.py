#!/usr/bin/env python3

from os import makedirs, getcwd as pwd, popen, remove
from os.path import join, exists
from shutil import copyfile, rmtree
import subprocess

def test():
    # prepare
    _cd = pwd()
    makedirs(join(_cd, 'testone'))

    copyfile(join(_cd, 'README.md'), join(_cd, 'testone', 'README.md'))

    # make exec
    subprocess.Popen(['dsfx', '-i', f"{join(_cd, 'testone')}", '-o', 'testonef', '-s', f"{join(_cd, 'test', 'demoset.py')}"]).wait()

    # check creation of file
    assert exists(join(_cd, 'testonef.dsfx')) == True
def test2():
    _cd = pwd()
    # re-open exec and check output as 'allok'
    assert popen(f"{join(_cd, 'testonef.dsfx')}").read().replace('\n','') == 'allok'

def test3():
    _cd = pwd()
    # check directory structure -> testonef/infs/demoset.py and testonef/infs/README.md
    assert exists(join(_cd, 'testonef', 'infs')) == True
    assert exists(join(_cd, 'testonef', 'infs', 'README.md')) == True
    assert exists(join(_cd, 'testonef', 'infs', 'demoset.py')) == True

def test4():
    _cd = pwd()
    # del all
    rmtree(join(_cd, 'testone'))
    rmtree(join(_cd, 'testonef'))
    remove(join(_cd, 'testonef.dsfx'))
    
    assert exists(join(_cd, 'testonef')) == False