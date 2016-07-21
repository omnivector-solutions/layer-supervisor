#!/usr/bin/python3
# Copyright (c) 2016, James Beedy <jamesbeedy@gmail.com>

import os
import subprocess as sp
from charms.reactive import status_set
from charmhelpers.core import host


class Supervisor:

    '''Class for supervisor utils
    '''

    def __init__(self, appname, ctxt={}):
        self.appname = appname
        self.ctxt = ctxt
        self.status_avail = '%s.supervisor.configured' % self.appname
        self.conf = '/etc/supervisor/conf.d/%s.conf' % self.appname
        self.tmpl = '%s.spvsr.conf' % self.appname
        self.cmds = {'start': 'supervisorctl start %s' % self.appname,
                     'stop': 'supervisorctl stop %s' % self.appname,
                     'reread': 'supervisorctl reread',
                     'update': 'supervisorctl update'}

    def start(self):
        '''Start supervisor
        '''
        sp.call(self.cmds['start'].split(), shell=False)

    def stop(self):
        '''Stop supervisor
        '''
        sp.call(self.cmds['stop'].split(), shell=False)

    def reread(self):
        '''Reread supervisor conf
        '''
        sp.call(self.cmds['reread'].split(), shell=False)

    def update(self):
        '''Update supervisor
        '''
        sp.call(self.cmds['update'].split(), shell=False)
        

    def render_supervisor_conf(self):

        """ Render /etc/supervisor/conf.d/{appname}.conf
            and restart supervisor process.
        """
        if os.path.exists(self.conf):
            sp.call(self.cmds['stop'].split(), shell=False)
            os.remove(self.conf)
        # Render supervisor conf
        render(source=self.tmpl,
               target=self.conf,
               owner='root',
               perms=0o644,
               context=self.ctxt)
        # Ensure supervisor is running
        if not host.service_running('supervisor'):
            host.service_start('supervisor')
        # Reread supervisor .conf and start/restart process
        self.reread()
        self.update()
        self.start()
        set_state(self.status_avail)
        
