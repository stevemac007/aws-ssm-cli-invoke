aws-ssm-cli-invoke
==================

.. image:: https://travis-ci.org/stevemac007/aws-ssm-cli-invoke.svg?branch=master
   :target: https://travis-ci.org/stevemac007/aws-ssm-cli-invoke
   :alt: Travis build badge

.. image:: https://coveralls.io/repos/github/stevemac007/aws-ssm-cli-invoke/badge.svg?branch=master
   :target: https://coveralls.io/github/stevemac007/aws-ssm-cli-invoke?branch=master
   :alt: Coveralls build badge

.. image:: https://img.shields.io/pypi/v/aws-ssm-invoke.svg
   :target: https://pypi.python.org/pypi/aws-ssm-invoke/
   :alt: PyPI version badge

A wrapper around an AWS SSM send-command that can optionally wait for
execution success.

Usage
-----

Usage on the tool can be found by executing ``aws-ssm-invoke -h``.

::

   $ aws-ssm-invoke -h
   usage: aws-ssm-invoke [-h] [--comment COMMENT]
                         (--instance-ids [INSTANCE_IDS [INSTANCE_IDS ...]] | --tags [TAGS [TAGS ...]])
                         [--wait] [--show-output]
                         command

   positional arguments:
     command               The command to execute on all matching EC2 instances

   optional xarguments:
     -h, --help            show this help message and exit
     --comment COMMENT
     --instance-ids [INSTANCE_IDS [INSTANCE_IDS ...]]
                           Instance ID's to execute on
     --tags [TAGS [TAGS ...]]
                           Key=Value pairs to execute on
     --wait                When supplied will poll the SSM command until it is
                           complete.
     --show-output         When supplied will show the output from each execution

Examples
--------

Wait
~~~~

Using the ``--wait`` flag polls for command status until complete and
shows the state.

.. code:: bash

   $ aws-ssm-invoke uptime --tags Name=database --wait
   Executed command 'uptime' - 486a3994-db41-4817-b741-f374cffec294  (Pending)
      - tag:Name = ['database']
    - Pending (Pending) [0 total, 0 complete, 0 error]
    - Success (NoInstancesInTag) [0 total, 0 complete, 0 error]

Show output
~~~~~~~~~~~

Some commands you want to see the output of, to do so specify the
``--show-output`` flag.

.. code:: bash

   $ aws-ssm-invoke uptime --tags Name=database --wait --show-output
   Executed command 'uptime' - 0b8deb73-2677-47a6-9167-a0889929d542  (Pending)
      - tag:Business:Application = ['ecommerce']
    - Pending (Pending) [0 total, 0 complete, 0 error]
    - Success (Success) [1 total, 1 complete, 0 error]
   Command output
    - [Success] i-0ddf60260170be3c7 (ip-172-31-9-100.ap-southeast-2.compute.internal)
    11:01:23 up 2 days,  5:41,  0 users,  load average: 0.00, 0.01, 0.05

Acknowledgements
~~~~~~~~~~~~~~~~

-  Project Bootstrapped from
   https://github.com/obi1kenobi/python-bootstrap
