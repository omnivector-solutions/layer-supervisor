# layer-supervisor

This layer provides Supervisor!

Supervisor is a process monitoring and control utility for UNIX-like operating systems.

# Usage

To use this layer in your charm or layer, simply include layer-supervisor in your `layer.yaml` like so:

```yaml
# layer.yaml
---
include: ['layer:supervisor']

...

```

You must also place a named supervisor template in your charm or layer's template directory. The template file should be named `<appname>.spvsr.conf`.

For example, if your appname is "myapp", your supervisor template would then be named `myapp.spvsr.conf`. This allows layer-supervisor to render your supervisor templates by only providing the appname, and/or context when instantiating the class, or calling the render conf function.


Once your template is in place, you can follow the simple usage example to get things started.

```python

from charms.supervisor import render_supervisor_conf


@when('myapp.installed')
@when('supervisor.available')
def start_myapp():
    render_supervisor_conf('myapp')

```
This layer will emit an `'<appname>.supervisor.available'` state specific to each app following the starting of the application specific supervisor process, you could then react to the `'<appname>.supervisor.available'` state from other layers, and throughout the rest of your layer or charm's lifecycle.

For example:

```python
import Workers


@when('myapp.supervisor.available')
def run_workers():
    w = Workers()
    w.start_tasks()

```

# Multi-Application Support

This layer is created in a way such that you may use it to control an arbitrary number of Supervisor managed applications. To support subsequent applications, all you need to do is; include the appropriately named template, instantiate a new Supervisor object, and call the render_supervisor_conf function!

Example
```python

from charms.supervisor import render_supervisor_conf
import Workers


@when('myapp1.installed')
@when('supervisor.available')
def start_myapp1():
    render_supervisor_conf('myapp1')


@when('myapp2.installed')
@when('supervisor.available')
def start_myapp2():
    render_supervisor_conf('myapp2')


@when('myapp1.supervisor.available',
      'myapp2.supervisor.available')
def run_workers():
    w = Workers()
    w.start_tasks()

```


# States
**supervisor.available** - This state is automatically emitted once Supervisor has been installed. Rely on this state to perform config rendering, and administrative ops when Supervisor is ready to be used.

**\<appname\>.supervisor.available** - This state is emitted after the successfull rendering of an application supervisor config, and starting of the supervisor <appname> process has completed.

### Contact
* [Supervisor Project](http://supervisord.org/)

### Copyright

Copyright &copy; 2016 James Beedy <jamesbeedy@gmail.com>

### License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
