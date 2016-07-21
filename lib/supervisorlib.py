import os
import subprocess as sp
from charms.reactive import set_state
from charmhelpers.core import host
from charmhelpers.core.templating import render


class Supervisor:

    '''Class for supervisor utils
    '''

    def __init__(self, appname):
        self.appname = appname
        self.status_avail = '%s.supervisor.available' % self.appname
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
        
    def render_supervisor_conf(self, ctxt={}):

        """ Render /etc/supervisor/conf.d/{appname}.conf
            and start the application supervisor process.

            :param ctxt: dictionary of context variables to render in
                         the template
        """
        if os.path.exists(self.conf):
            self.stop()
            os.remove(self.conf)
        # Render supervisor conf
        render(source=self.tmpl,
               target=self.conf,
               owner='root',
               perms=0o644,
               context=ctxt)
        # Ensure supervisor is running
        if not host.service_running('supervisor'):
            host.service_start('supervisor')
        # Reread supervisor .conf and start/restart process
        self.reread()
        self.update()
        self.start()
        set_state(self.status_avail)
