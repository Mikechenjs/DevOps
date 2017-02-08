# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 07 14:41
# Author Yo
# Email YoLoveLife@outlook.com
from util import FTP
from modules.persontask import PersonTask
from modules.personbook import PersonBook
from modules.personblock import PersonBlock
def nginx_installplaybook(server='other',version='1.10.1',prefix='/usr/local',checksum='088292d9caf6059ef328aa7dda332e44'):
    _ext_vars = {
        'version': checksum,
        'prefix': checksum,
        'basedir': '{{prefix}}/nginx',
        'file': 'nginx-{{version}}.tar.gz',
        'fro': 'http://%s/package/nginx/{{file}}' % FTP,
        'checksum': checksum,
        'user':'nginx',
    }

    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("install nginx",server, 'no')
    task1 = PersonTask(module="get_url", args="checksum=md5:{{checksum}} url={{fro}} dest=~", )
    task2 = PersonTask(module="script",
                       args="../../scripts/nginx/nginx_install.sh -v {{version}} -f {{prefix}} -u {{user}}", )
    task3 = PersonTask(module="file", args="dest=~/{{file}} state=absent", )
    pb.add_task(task1)
    pb.add_task(task2)
    pb.add_task(task3)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_removeplaybook(server='other',prefix='/usr/local',):
    _ext_vars = {
        'prefix': '/usr/local',
        'basedir': '{{prefix}}/nginx',
        'user':'nginx',
    }

    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("remove nginx",server, 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/nginx/nginx_remove.sh -f {{prefix}} -u {{user}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_controlplaybook(server='other',control='start',pid='/usr/local/nginx/logs/nginx.pid'):
    _ext_vars = {
        'control':control,
        'pid':pid
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("control nginx", server, 'no')
    task1 = PersonTask(module="script",
                       args="../../scripts/nginx/nginx_control.sh {{control}} {{pid}}", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()

def nginx_configureplaybook(server='other',prefix='/usr/local',workproc='1',pid='logs/nginx.pid',workconn='1024',port='80',servername='localhost',locations=''):
    _ext_vars = {
        'prefix':prefix,
        'basedir':'{{prefix}}/nginx',
        'user':'nginx',
        'workproc':workproc,
        'pid':pid,
        'workconn':workconn,
        'port':port,
        'servername':servername,
        'locations':locations,
    }
    personblock = PersonBlock()
    personblock.add_extendvars(_ext_vars)
    pb = PersonBook("configure nginx", server, 'no')
    task1 = PersonTask(module="template",
                   args="dest={{basedir}}/conf/nginx.conf src=../../template/nginx.j2 owner=nginx group=nginx mode=644", )
    pb.add_task(task1)
    personblock.set_playbook(pb)
    personblock.run_block()
if __name__=='__main__':
    nginx_removeplaybook(server='nginx-server')
    nginx_installplaybook(server='nginx-server')
    nginx_configureplaybook(server='nginx-server')
    nginx_controlplaybook(server='nginx-server',control='start')