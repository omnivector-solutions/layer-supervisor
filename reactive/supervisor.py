from charms.reactive import set_state
from charms.reactive import when
from charms.reactive import when_not
from charmhelpers.core import hookenv

from charms import apt


@when_not('supervisor.available')
def install_supervisor():
    '''Install supervisor
    '''
    hookenv.status_set('maintenance', 'installing Supervisor')
    apt.queue_install(['supervisor'])


@when('apt.installed.supervisor')
@when_not('supervisor.available')
def supervisor_avail():
    hookenv.status_set('active', 'Supervisor available')
    set_state('supervisor.available')
