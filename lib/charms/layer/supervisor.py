import os
import subprocess as sp
from charms.reactive import set_state
from charmhelpers.core import host
from charmhelpers.core.templating import render


def start(appname):
    """Start supervisor
    """
    sp.call(("supervisorctl start %s" % appname).split(), shell=False)


def stop(appname):
    """Stop supervisor
    """
    sp.call(("supervisorctl stop %s" % appname).split(), shell=False)


def reread(appname):
    """Reread supervisor conf
    """
    sp.call(("supervisorctl reread %s" % appname).split(), shell=False)


def update(appname):
    """Update supervisor
    """
    sp.call(("supervisorctl update %s" % appname).split(), shell=False)
        

def render_supervisor_conf(appname, ctxt={}):
    """ Render /etc/supervisor/conf.d/{appname}.conf
        and start the application supervisor process.


        :param ctxt: dictionary of context variables to render in
                     the template
    """
    spvsr_avail = "%s.supervisor.available" % appname
    spvsr_conf = "/etc/supervisor/conf.d/%s.conf" % appname
    spvsr_tmpl = "%s.spvsr.conf" % appname
    if os.path.exists(spvsr_conf):
        stop()
        os.remove(spvsr_conf)
    # Render supervisor conf
    render(source=spvsr_tmpl,
           target=spvsr_conf,
           owner="root",
           perms=0o644,
           context=ctxt)
    # Ensure supervisor is running
    if not host.service_running("supervisor"):
        host.service_start("supervisor")
    # Reread supervisor .conf and start/restart process
    reread()
    update()
    start()
    set_state(spvsr_avail)
