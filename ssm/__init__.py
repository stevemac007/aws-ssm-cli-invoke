from __future__ import absolute_import

from ssm.main import SSMInvoke
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--command", required=True)
    parser.add_argument("--comment", required=False)

    parser.add_argument('--instance-ids', nargs='*', help='Instance ID\'s to execute on', required=False)
    parser.add_argument('--tags', nargs='*', help='Key,Value pairs to execute on', required=False)

    parser.add_argument("--wait", action="store_true", required=False, default=False)
    parser.add_argument("--show-output", action="store_true", required=False, default=False)
    parser.add_argument("--ignore-fail-on-no-tag", action="store_true", required=False, default=False)

    args = parser.parse_args()

    invoker = SSMInvoke()
    invoker.parse_args(args)
    invoker.invoke()