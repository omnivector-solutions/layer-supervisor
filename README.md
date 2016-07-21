# layer-supervisor

This layer provides Supervisor! Supervisor is a process monitoring and control utility for UNIX-like operating systems.

To use this layer in your charm or layer, simply include layer-supervisor in your `layer.yaml` like so:

```yaml
# layer.yaml
---
include: ['layer:supervisor']

...

```

You must also place a named supervisor template in your charm or layer's template directory. The template file should be named like so:

```
<appname>.spvsr.conf
```

For example, if your appname is "froggy", your supervisor template would then be named `froggy.spvsr.conf`. This allows layer-supervisor to render your supervisor templates by only providing the appname, and/or context when instantiating the class.


Once your template is in place, you can follow the simple usage example to get things started (this example assumes you provide the context to the templates).

```python

from supervisorlib import Supervisor


@when('apps.installed')
@when('supervisor.available')
def start_apps():

    for app in applist:
        spvsr = Supervisor(app)
        spvsr.render_supervisor_conf()

```

This layer will emit an `'<appname>.supervisor.available'` spicific to each app, after each app has started. This state is emitted following the starting of the supervisor process for a service by the render_supervisor_conf function. You could then react to the `'<appname>.supervisor.available'` state throughout the rest of your layer or charm. 

For example:

```python

@when('myapp.supervisor.available')
def run_workers():
    w = Workers()
    w.start_tasks()

```


# emitters

**supervisor.available** - This state is automatically emitted once Supervisor has been installed. Rely on this state to perform config rendering, and administrative ops when Supervisor is ready to be used.

**<appname>.supervisor.available** - This state is emitted after the successfull rendering of an application supervisor config template, and starting of the supervisor <appname> process has completed.
