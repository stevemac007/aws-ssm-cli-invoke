# aws-ssm-cli-invoke

[![Build Status](https://travis-ci.org/stevemac007/aws-ssm-cli-invoke.svg?branch=master)](https://travis-ci.org/stevemac007/aws-ssm-cli-invoke)

A wrapper around an AWS SSM send-command that can optionally wait for execution success.

## Usage

Usage on the tool can be found by executing `aws-ssm-invoke -h`.

```
$ aws-ssm-invoke --help
usage: aws-ssm-invoke [-h] [--comment COMMENT]
                      (--instance-ids [INSTANCE_IDS [INSTANCE_IDS ...]] | --tags [TAGS [TAGS ...]])
                      [--wait] [--show-output]
                      command

positional arguments:
  command               The command to execute on all matching EC2 instances

optional arguments:
  -h, --help            show this help message and exit
  --comment COMMENT
  --instance-ids [INSTANCE_IDS [INSTANCE_IDS ...]]
                        Instance ID's to execute on
  --tags [TAGS [TAGS ...]]
                        Key=Value pairs to execute on
  --wait                When supplied will poll the SSM command until it is
                        complete.
  --show-output         When supplied will show the output from each execution
```

## Example

```
$ aws-ssm-invoke uptime --tags Name=database --wait
Executed command 'uptime' - 486a3994-db41-4817-b741-f374cffec294  (Pending)
   - tag:Name = ['database']
 - Pending (Pending) [0 total, 0 complete, 0 error]
 - Success (NoInstancesInTag) [0 total, 0 complete, 0 error]
```

### Acknowledgements

- Project Bootstrapped from https://github.com/obi1kenobi/python-bootstrap