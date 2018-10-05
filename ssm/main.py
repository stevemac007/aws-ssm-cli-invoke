from __future__ import absolute_import, print_function

import argparse
import sys
import time

import boto3


class SSMInvoke(object):

    SUCCESS_STATES = ["Success"]
    ERROR_STATES = ["Failed"]
    ERROR_DETAIL_STATES = ["NoInstancesInTag"]

    def __init__(self):
        """Object constructor, sets defaults."""
        self.targets = []
        self.command = None
        self.instances = None
        self.comment = ""
        self.ssm_client = None
        self.wait = False
        self.show_output = False

    def parse_args(self, parsed_args):
        """Convert the argsparser arguments into the internal representation required for the SSM commands and logic flow.

        :param parsed_args:
        :return:
        """
        self.command = parsed_args.command
        self.wait = parsed_args.wait
        self.show_output = parsed_args.show_output

        if parsed_args.tags is not None:
            for tag in parsed_args.tags:
                vals = tag.split('=')
                key = vals[0]
                value = vals[1]

                self.targets += [
                    {
                        'Key': "tag:" + key,
                        'Values': [value]
                    }
                ]

        if parsed_args.comment is not None:
            self.comment = parsed_args.comment

    def _ssm_client(self):

        if self.ssm_client is None:
            self.ssm_client = boto3.client('ssm')

        return self.ssm_client

    def invoke(self):
        """Perform the actual SSM calls and console output.

        :return:
        """
        command_result = self._ssm_client().send_command(Targets=self.targets,
                                                         InstanceIds=[],
                                                         DocumentName='AWS-RunShellScript',
                                                         Comment=self.comment,
                                                         Parameters={"commands": [self.command]})

        command_id = command_result["Command"]["CommandId"]
        status = command_result["Command"]["Status"]

        print("Executed command '{}' - {}  ({})".format(self.command, command_id, status))

        for tag in self.targets:

            key = tag["Key"]
            value = tag["Values"]

            print("   - {} = {}".format(key, value))

        if self.wait or self.show_output:

            not_done = True
            in_error = False

            while not_done:
                results = self._ssm_client().list_commands(CommandId=command_id)

                for result in results["Commands"]:
                    status = result['Status']
                    status_details = result['StatusDetails']
                    target_count = result['TargetCount']
                    target_complete = result['CompletedCount']
                    target_error = result["ErrorCount"]

                    print(" - {} ({}) [{} total, {} complete, {} error]".format(status, status_details, target_count,
                                                                                target_complete, target_error))

                    if status in self.SUCCESS_STATES:
                        not_done = False

                        if status_details in self.ERROR_DETAIL_STATES:
                            in_error = True

                    elif status in self.ERROR_STATES:
                        not_done = False
                        in_error = True

                if not_done:
                    time.sleep(5)

            if self.show_output:
                print("Command output")

                response = self._ssm_client().list_command_invocations(CommandId=command_id)

                for invocation in response["CommandInvocations"]:
                    instance_id = invocation['InstanceId']
                    instance_name = invocation['InstanceName']
                    status = invocation['Status']

                    response = self._ssm_client().get_command_invocation(
                        CommandId=command_id,
                        InstanceId=instance_id
                    )

                    elapsed_time = response["ExecutionElapsedTime"]
                    response_code = response["ResponseCode"]

                    standard_output_content = response["StandardOutputContent"]
                    standard_error_content = response["StandardErrorContent"]

                    print(" - [{} in {}] {} ({})".format(status, elapsed_time, instance_id, instance_name))
                    if response_code == 0:
                        print(standard_output_content)
                    else:
                        print(standard_error_content)

            if in_error:
                sys.exit(1)


def main():
    """Entry point for command line.

    :return:
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--comment", required=False)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--instance-ids', nargs='*', required=False,
                       help='Instance ID\'s to execute on')
    group.add_argument('--tags', nargs='*', required=False,
                       help='Key=Value pairs to execute on')

    parser.add_argument("--wait", action="store_true", required=False, default=False,
                        help="When supplied will poll the SSM command until it is complete.")
    parser.add_argument("--show-output", action="store_true", required=False, default=False,
                        help="When supplied will show the output from each execution")

    parser.add_argument("command",
                        help="The command to execute on all matching EC2 instances")

    # parser.add_argument("--ignore-fail-on-no-tag", action="store_true", required=False, default=False)

    args = parser.parse_args()

    invoker = SSMInvoke()
    invoker.parse_args(parsed_args=args)
    invoker.invoke()


if __name__ == '__main__':
    main()
