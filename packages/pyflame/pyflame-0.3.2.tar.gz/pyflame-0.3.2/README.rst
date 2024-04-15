..
  Copyright 2020-2022 Daniel Harding
  Distributed as part of the pyflame project under the terms of the MIT license

Generate flamegraphs for Python code, using Brendan Gregg's excellent FlameGraph_
project to perform the heavy lifting.

pyflame can be used to invoke a Python script from the command line and generate a
flamegraph of its execution.  It also provides a panel for `Django Debug Toolbar`_ that
generates a flamegraph for each request, as well as an IPython_ extension that provides
a cell magic to generate flamegraphs for display within a `Jupyter Notebook`_.

Basic Installation
------------------

* Run ``python -m pip install pyflame``.

* Download flamegraph.pl_ and then either:

  - make it available via the ``PATH`` environment variable, or
  - set up the appropriate configuration as described below to indicate where the script
    is located on the filesystem.

Command Line Usage
------------------

Invoke using ``python -m pyflame [<options>] <script> [<args>]``.

The following options are supported:

* ``-p path``, ``--flamegraph-script-path path``: the path to the flamegraph.pl_ script
  (if not specified, search using the ``PATH`` environment variable).
* ``-a arg_string``, ``--flamegraph-extra-args arg_string``: a string specifying extra
  command line arguments to pass when invoking flamegraph.pl.
* ``-s interval``, ``--sample-interval interval``: the amount of time the sampler thread
  will wait between capturing stack traces, in seconds (default: 0.001).
* ``-o path``, ``--output-file path``: the location to save the flamegraph. If not
  specified, save in the current directory using the name of the Python script with an
  ``.svg`` extension appended.

Django Debug Toolbar Configuration
----------------------------------

To enable, add ``pyflame`` to ``INSTALLED_APPS`` and
``pyflame.djdt.panel.FlamegraphPanel`` to ``DEBUG_TOOLBAR_PANELS`` in the
project's Django settings module.

pyflame uses a similar configuration mechanism to that of Django Debug Toolbar.  To
modify the default configuration, add a ``PYFLAME_CONFIG`` setting to the project's
Django settings module. This must be a dictionary which may contain any of the following
options:

* ``FLAMEGRAPH_SCRIPT_PATH``

  Default: ``None``

  The path to the flamegraph.pl_ script. The default of ``None`` tells pyflame to search
  for flamegraph.pl using the ``PATH`` environment variable.

* ``FLAMEGRAPH_SCRIPT_EXTRA_ARGS``

  Default: ``[]``

  A list of extra command line arguments to pass when invoking flamegraph.pl.

* ``SAMPLE_INTERVAL``

  Default: ``0.001``,

  The amount of time the sampler thread will wait between capturing stack traces, in
  seconds.

Jupyter Notebook Configuration
------------------------------

To enable the ``%%pyflame`` magic within an IPython kernel running under Jupyter
Notebook, first load the IPython extension using the ``%load_ext`` magic::

    In [1]: %load_ext pyflame

To load the extension automatically each time the IPython kernel starts, list it in the
``ipython_config.py`` file::

    c.InteractiveShellApp.extensions = [
        'pyflame'
    ]

There are three other configuration attributes that can be set to configure the
extension:

* ``PyFlameMagic.flamegraph_script_path``

  Default: ``None``

  The path to the flamegraph.pl_ script. The default of ``None`` tells pyflame to search
  for flamegraph.pl using the ``PATH`` environment variable.

* ``PyFlameMagic.flamegraph_script_extra_args``

  Default: ``[]``

  A list of extra command line arguments to pass when invoking flamegraph.pl.

* ``PyFlameMagic.default_sample_interval``

  Default: ``0.001``

  The amount of time the sampler thread will wait between capturing stack traces, in
  seconds.

Licensing
---------

pyflame is distributed under the terms of the `MIT license`_.  A copy of the license
text is avaiable in the LICENSE_ file.

Credits
-------

pyflame could not exist without the work of Brendan Gregg and other contributors to
create FlameGraph_. pyflame also draws inspiration from two related projects. The
original idea was inspired by Bo Lopker's djdt-flamegraph_ project (pyflame actually
started out as a fork of djdt-flamegraph, but over time I ended up completely rewriting
it).  The approach of spawning a separate thread to sample stack traces using
``sys._current_frames()`` was drawn from Evan Hempel's python-flamegraph_ project.

.. _FlameGraph: https://github.com/brendangregg/FlameGraph
.. _Django Debug Toolbar: https://github.com/jazzband/django-debug-toolbar
.. _IPython: https://ipython.readthedocs.io/en/stable/overview.html
.. _Jupyter Notebook: https://jupyter-notebook.readthedocs.io/en/stable/
.. _flamegraph.pl: https://github.com/brendangregg/FlameGraph/blob/master/flamegraph.pl
.. _MIT license: https://opensource.org/licenses/MIT
.. _LICENSE: https://gitlab.com/living180/pyflame/-/blob/main/LICENSE
.. _djdt-flamegraph: https://github.com/23andMe/djdt-flamegraph
.. _python-flamegraph: https://github.com/evanhempel/python-flamegraph
