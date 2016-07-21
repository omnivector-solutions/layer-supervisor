from charms.reactive import set_state
from charms.reactive import when
from charms.reactive import when_not
from charmhelpers.core import hookenv
from charmhelpers.fetch import apt_install


@when_not('supervisor.installed')
def install_supervisor():
    '''Install supervisor
    '''
    hookenv.status_set('maintenance', 'installing Supervisor')
    apt_install(['supervisor'])
    set_state('supervisor.installed')


@when('supervisor.installed')
@when_not('supervisor.available')
def supervisor_avail():
    hookenv.status_set('active', 'Supervisor available')
    set_state('supervisor.available')
