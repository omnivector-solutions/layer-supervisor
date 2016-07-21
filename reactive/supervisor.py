from charms.reactive import set_state
from charms.reactive import when_not
from charmhelpers.core import hookenv


@when_not("supervisor.available")
def supervisor_avail():
    """Set supervisor.available
    """
    hookenv.status_set("maintenance", "installing Supervisor")
    set_state("supervisor.available")
